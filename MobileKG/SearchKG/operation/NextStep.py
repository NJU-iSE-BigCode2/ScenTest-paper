from MobileKG.SearchKG.po.Node import Node
from MobileKG.Neo4j.GraphSearch import GraphSearch
from MobileKG.SearchKG.po.Component import Component
from MobileKG.GenerateKG.operation.MessageCompare import MessageCompare
from MobileKG.Config.RunConfig import *
from MobileKG.SearchKG.po.Layout import Layout
from MobileKG.LayoutAnalysis.LayoutMain import match
import json


class NodeComponent:
    def __init__(self, node, component, rate):
        self.node = node
        self.component = component
        self.rate = rate
        return


class NextStep:
    layout_config_path = '../Config/TypicalLayoutConfig.json'
    LAYOUT = json.loads(open(layout_config_path, 'r', encoding='utf-8').read())[graph_type]
    layouts = []
    for l in LAYOUT:
        layouts.append(Layout(l))
    search_policy_config_path = '../Config/SearchPolicy.json'
    search_policy = json.loads(open(search_policy_config_path, 'r', encoding='utf-8').read())[graph_type]

    def __init__(self, picture, split):
        self.picture = picture
        self.split = split
        return

    def search_with_head(self, components_dic, head_id):
        if head_id == 0:
            nodes = GraphSearch.get_head_nodes()
        else:
            nodes = GraphSearch.get_next_nodes(head_id)

        for n in nodes:
            print(n.opt.name + ' ' + n.name)

        components = self.change_to_components(components_dic)

        result = self.generate_next(nodes, components)
        return result

    def search_all(self, components_dic):
        nodes = GraphSearch.get_all_nodes()

        components = self.change_to_components(components_dic)

        result = self.generate_next(nodes, components)
        return result

    def change_to_components(self, components_dic):
        components = []
        for item in components_dic['components']:
            c = Component(item)
            components.append(c)
        return components

    def generate_next(self, nodes, components):
        if nodes is None or components is None or len(nodes) == 0 or len(components) == 0:
            return {
                'status': 'failed',
                'data': None
            }

        pairs = self.find_valid_components(nodes, components)
        result_dic = {}
        for pair in pairs:
            c: Component = pair.component
            n: Node = pair.node
            key = str(c.x1) + ',' + str(c.y1) + ',' + str(c.x2) + ',' + str(c.y2)
            if key not in result_dic.keys():
                result_dic[key] = pair
            else:
                if result_dic[key].rate < pair.rate:
                    result_dic[key] = pair
        result = []
        for pair_key in result_dic:
            c: Component = result_dic[pair_key].component
            n: Node = result_dic[pair_key].node
            c.operation = n.opt.name
            c.cnt = n.name
            c.cnt_id = n.id
            c.state = n.state
            result.append(c.to_dic())

        return {
            'status': 'success',
            'data': result
        }

    def find_valid_components(self, nodes, components):
        result = []
        for n in nodes:
            related_l = None
            related_l_similarity = 0
            for l in NextStep.layouts:
                similar_rate = self.compare_node_layout(n, l)
                if similar_rate > valid_layout_threshold and similar_rate > related_l_similarity:
                    related_l = l
                    related_l_similarity = similar_rate
            if related_l is not None:
                x, y, w, h, rx, ry = match(related_l, self.picture, self.split)
                center_x = w * rx + x
                center_y = h * ry + y
                c = self.find_com_by_layout(center_x, center_y, components)
                if c is not None:
                    temp = NodeComponent(n, c, related_l_similarity)
                    result.append(temp)
                    if self.search_policy['type'] == 'layout':
                        continue
                elif self.search_policy['layout_sensitive'] == 'TRUE':
                    temp_c = Component({
                        'category': 'ImageView',
                        'x1': int(center_x),
                        'y1': int(center_y),
                        'x2': int(center_x) + 5,
                        'y2': int(center_y) + 5,
                        'ocr': '此布局无文本与之对应'
                    })
                    temp = NodeComponent(n, temp_c, related_l_similarity)
                    result.append(temp)

            related_c = None
            related_c_similarity = 0
            for c in components:
                similar_rate = self.compare_node_com(n, c)
                if similar_rate > valid_component_threshold and similar_rate > related_c_similarity:
                    related_c = c
                    related_c_similarity = similar_rate
            if related_c is not None:
                temp = NodeComponent(n, related_c, related_c_similarity)
                result.append(temp)
        return result

    def compare_node_com(self, node: Node, component: Component):
        if node is None or component is None:
            return 0
        if component.ocr is None or component.ocr == '':
            return 0

        widget_sim = 0
        if node.widget is not None and node.widget.english == component.category:
            widget_sim = 1
        cnt_sim = MessageCompare.txt_sim(node.name, component.ocr)
        if node.opt is not None:
            opt_cnt_sim = MessageCompare.txt_sim(node.opt.name + node.name, component.ocr)
            if opt_cnt_sim > cnt_sim:
                cnt_sim = opt_cnt_sim

        ocr_sim = 0
        for ocr in node.ocr:
            temp = MessageCompare.txt_sim(ocr.name, component.ocr)
            if temp > ocr_sim:
                ocr_sim = temp

        return widget_sim * node_com_wid_sim_rate + cnt_sim * node_com_cnt_sim_rate + ocr_sim * node_com_ocr_sim_rate

    def compare_node_layout(self, node: Node, layout: Layout):
        if node is None or layout is None:
            return 0

        widget_sim = 0
        if node.widget is not None and node.widget.english == layout.widget:
            widget_sim = 1
        cnt_sim = MessageCompare.txt_sim(node.name, layout.cnt)
        if node.opt is not None:
            opt_cnt_sim = MessageCompare.txt_sim(node.opt.name + node.name, layout.opt + layout.cnt)
            if opt_cnt_sim > cnt_sim:
                cnt_sim = opt_cnt_sim

        ocr_sim = 0
        for ocr in node.ocr:
            temp = MessageCompare.txt_sim(ocr.name, layout.ocr)
            if temp > ocr_sim:
                ocr_sim = temp

        return widget_sim * node_layout_wid_sim_rate + cnt_sim * node_layout_cnt_sim_rate + ocr_sim * node_layout_ocr_sim_rate

    def find_com_by_layout(self, x, y, components):
        result = None
        for c in components:
            if c.x1 <= x <= c.x2 and c.y1 <= y <= c.y2:
                if result is None:
                    result = c
                else:
                    if (c.x2 - c.x1) * (c.y2 - c.y1) < (result.x2 - result.x1) * (result.y2 - result.y1):
                        result = c
        return result
