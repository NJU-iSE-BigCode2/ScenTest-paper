from py2neo import Graph, Node
from MobileKG.GenerateKG.po.Content import Content
from MobileKG.GenerateKG.po.OCRTex import OCRTex
from MobileKG.GenerateKG.po.Widget import Widget
from MobileKG.GenerateKG.po.Opt import Opt
from MobileKG.SearchKG.po.Node import Node


class GraphSearch:
    graph = Graph('http://localhost:7474', auth=('neo4j', 'neo4j'))

    @classmethod
    def get_all_contents(cls):
        cypher = 'match(c:Content) return c'
        data = GraphSearch.graph.run(cypher).data()
        cnts = []
        for item in data:
            cnts.append(GraphSearch.get_content(item['c']['id']))
        return cnts

    @classmethod
    def get_content(cls, cnt_id):
        cypher = 'match (c:Content) where c.id=' + str(cnt_id) + ' return c'
        data = GraphSearch.graph.run(cypher).data()
        cnt = Content(cnt_id, data[0]['c']['name'], data[0]['c']['english'], [],
                      GraphSearch.get_content_operation(cnt_id),
                      GraphSearch.get_content_widget(cnt_id),
                      None,
                      GraphSearch.get_content_ocr(cnt_id))
        return cnt

    @classmethod
    def get_content_ocr(cls, cnt_id):
        cypher = 'match (c:Content)-[r1:CNT_OCR_REL]->(ocr:OCRText) where c.id=' + str(cnt_id) + ' return c,ocr'
        data = GraphSearch.graph.run(cypher).data()
        if len(data) == 0:
            return None
        ocr = OCRTex(data[0]['ocr']['id'], data[0]['ocr']['name'], [])
        return ocr

    @classmethod
    def get_content_ocrs(cls, cnt_id):
        cypher = 'match (c:Content)-[r1:CNT_OCR_REL]->(ocr:OCRText) where c.id=' + str(cnt_id) + ' return c,ocr'
        data = GraphSearch.graph.run(cypher).data()
        result = []
        for i in range(0, len(data)):
            ocr = OCRTex(data[i]['ocr']['id'], data[i]['ocr']['name'], [])
            ocr.similar = GraphSearch.get_ocr_similar(ocr.id)
            result.append(ocr)
        return result

    @classmethod
    def get_content_widget(cls, cnt_id):
        cypher = 'match (c:Content)-[r1:CNT_WID_REL]->(wdg:Widget) where c.id=' + str(cnt_id) + ' return c,wdg'
        data = GraphSearch.graph.run(cypher).data()
        if len(data) == 0:
            return None
        wdg = Widget(data[0]['wdg']['id'], data[0]['wdg']['name'], data[0]['wdg']['english'])
        return wdg

    @classmethod
    def get_content_operation(cls, cnt_id):
        cypher = 'match (c:Content)-[r1:CNT_OPT_REL]->(opt:Operation) where c.id=' + str(cnt_id) + ' return c,opt'
        data = GraphSearch.graph.run(cypher).data()
        if len(data) == 0:
            return None
        opt = Opt(data[0]['opt']['id'], data[0]['opt']['name'], data[0]['opt']['english'])
        return opt

    @classmethod
    def get_similar_content(cls, cnt_id):
        cypher = 'match(c1:Content)-[r:CNT_REL{relation:"相似"}]->(c2:Content) where c1.id=' + str(cnt_id) + ' return c2'
        data = GraphSearch.graph.run(cypher).data()
        result = []
        for item in data:
            invalid = GraphSearch.exist_cnt_next_cnt(cnt_id, item['c2']['id']) or GraphSearch.exist_cnt_next_cnt(
                item['c2']['id'],
                cnt_id)
            if not invalid:
                result.append(GraphSearch.get_content(item['c2']['id']))
        return result

    @classmethod
    def exist_cnt_next_cnt(cls, cnt1_id, cnt2_id):
        cypher = 'match (c1:Content)-[r:CNT_REL]->(c2:Content) where c1.id=' + str(cnt1_id) + ' and c2.id=' + str(
            cnt2_id) + ' and r.relation="后继" return r'
        data = GraphSearch.graph.run(cypher).data()
        if len(data) > 0:
            return True
        else:
            return False

    @classmethod
    def get_all_ocrs(cls):
        cypher = 'match (o:OCRText) return o'
        data = GraphSearch.graph.run(cypher).data()
        result = []
        for item in data:
            result.append(GraphSearch.get_ocr(item['o']['id']))
        return result

    @classmethod
    def get_ocr(cls, ocr_id):
        cypher = 'match(o:OCRText) where o.id=' + str(ocr_id) + ' return o'
        data = GraphSearch.graph.run(cypher).data()
        if len(data) > 0:
            ocr = OCRTex(data[0]['o']['id'], data[0]['o']['name'], GraphSearch.get_ocr_similar(ocr_id))
            return ocr
        else:
            return None

    @classmethod
    def get_ocr_similar(cls, ocr_id):
        cypher = 'match (o1:OCRText)-[r:OCR_REL{relation:"相似"}]->(o2:OCRText) where o1.id=' + str(ocr_id) + ' return o2'
        data = GraphSearch.graph.run(cypher).data()
        result = []
        for item in data:
            temp = OCRTex(item['o2']['id'], item['o2']['name'], [])
            result.append(temp)
        return result

    @classmethod
    def get_widget(cls, wid_id):
        cypher = 'match(wid:Widget) where wid.id=' + str(wid_id) + ' return wid'
        data = GraphSearch.graph.run(cypher).data()
        result = None
        if len(data) != 0:
            result = Widget(int(data[0]['wid']['id']), data[0]['wid']['name'], data[0]['wid']['english'])
        return result

    @classmethod
    def get_opt(cls, opt_id):
        cypher = 'match(opt:Operation) where opt.id=' + str(opt_id) + ' return opt'
        data = GraphSearch.graph.run(cypher).data()
        result = None
        if len(data) != 0:
            result = Opt(int(data[0]['opt']['id']), data[0]['opt']['name'], data[0]['opt']['english'])
        return result

    @classmethod
    def exist_ocr_ocr(cls, ocr_id1, ocr_id2):
        cypher = 'match (ocr1:OCRText)-[r:OCR_REL]->(ocr2:OCRText) where ocr1.id=' + str(
            ocr_id1) + ' and ocr2.id=' + str(ocr_id2) + ' return r'
        data = GraphSearch.graph.run(cypher).data()
        if len(data) > 0:
            return True
        else:
            return False

    @classmethod
    def exist_cnt_next_cnt(cls, cnt_id1, cnt_id2):
        cypher = 'match (cnt1:Content)-[r:CNT_REL]->(cnt2:Content) where cnt1.id=' + str(
            cnt_id1) + ' and cnt2.id=' + str(cnt_id2) + ' and r.relation="后继" return cnt1'
        data=GraphSearch.graph.run(cypher).data()
        if len(data)>0:
            return True
        else:
            return False

    @classmethod
    def get_next_nodes(cls, cnt_id):
        # 1.先找到当前节点的相似节点
        current_similar = GraphSearch.get_similar_content(cnt_id)
        current_similar.append(GraphSearch.get_content(cnt_id))

        # 2.将这些节点的后继都添加进来,并删去相同的节点
        next_nodes = []
        next_nodes_ids = []
        for c_s in current_similar:
            cypher = 'match (cnt1:Content)-[r:CNT_REL{relation:"后继"}]->(cnt2:Content) where cnt1.id=' + str(
                c_s.id) + ' return cnt2'
            data = GraphSearch.graph.run(cypher).data()
            for i in range(0, len(data)):
                cnt2_id = data[i]['cnt2']['id']
                if cnt2_id not in next_nodes_ids:
                    next_nodes_ids.append(cnt2_id)
                    node = GraphSearch.get_node(cnt2_id)
                    next_nodes.append(node)

        # 3.将所有后继的相似节点也添加进结果集
        for n_n in next_nodes:
            similar_contents = n_n.similar
            for s_c in similar_contents:
                if s_c.id not in next_nodes_ids:
                    next_nodes_ids.append(s_c.id)
                    next_nodes.append(GraphSearch.get_node(s_c.id))

        return next_nodes

    @classmethod
    def get_node(cls, cnt_id):
        cypher = 'match (cnt:Content) where cnt.id=' + str(cnt_id) + ' return cnt'
        data = GraphSearch.graph.run(cypher).data()
        result = None
        if len(data) > 0:
            result = Node(int(data[0]['cnt']['id']), data[0]['cnt']['name'], data[0]['cnt']['english'],
                          GraphSearch.get_similar_content(cnt_id),
                          GraphSearch.get_content_operation(cnt_id),
                          GraphSearch.get_content_widget(cnt_id),
                          None,
                          GraphSearch.get_content_ocrs(cnt_id)
                          )
            if data[0]['cnt']['tail'] is not None and data[0]['cnt']['tail'] == 'True':
                result.state = 'T'
            else:
                result.state = 'M'
        return result

    @classmethod
    def get_head_nodes(cls):
        # cypher = 'match (cnt1:Content)-[r:CNT_REL{relation:"后继"}]->(cnt2:Content) return cnt2'
        # data = Search.graph.run(cypher).data()
        # cnt2_ids = []
        # for i in range(0, len(data)):
        #     cnt2_ids.append(int(data[i]['cnt2']['id']))
        # cnts = Search.get_all_contents()
        # result = []
        # for cnt in cnts:
        #     if cnt.id not in cnt2_ids:
        #         result.append(Search.get_node(cnt.id))
        cypher = 'match (c:Content) where c.head="True" return c'
        data = GraphSearch.graph.run(cypher).data()
        result = []
        for i in range(0, len(data)):
            result.append(GraphSearch.get_node(int(data[i]['c']['id'])))
        return result

    @classmethod
    def get_all_nodes(cls):
        cypher = 'match (c:Content) return c'
        data = GraphSearch.graph.run(cypher).data()
        result = []
        for i in range(0, len(data)):
            result.append(GraphSearch.get_node(data[i]['c']['id']))
        return result
