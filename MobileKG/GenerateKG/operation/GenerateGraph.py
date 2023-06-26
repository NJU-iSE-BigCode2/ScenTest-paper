import os
import json
from MobileKG.GenerateKG.po.Widget import Widget
from MobileKG.GenerateKG.po.Opt import Opt
from MobileKG.GenerateKG.po.OCRTex import OCRTex
from MobileKG.GenerateKG.po.Content import Content
from MobileKG.GenerateKG.operation.MessageCompare import MessageCompare
from MobileKG.Neo4j.GraphAdd import GraphAdd

class GenerateGraph:
    def __init__(self, dir):
        self.__widgets = {}
        self.__opts = {}
        self.__ocrs: list[OCRTex] = []
        self.__dir = dir
        return

    def execute(self):
        self.__generate_widget()
        self.__generate_operation()
        self.__generate_ocr()
        self.__generate_cnt()
        return

    def __generate_widget(self):
        GraphAdd.current_scene = 'widgets'
        file = open(self.__dir + 'widgets.json', 'r', encoding='utf-8')
        data = json.loads(file.read())
        self.__widgets = {}
        for wid_dic in data:
            temp = Widget(0, '', '')
            temp.from_dic(wid_dic)
            self.__widgets[temp.english] = temp
        GraphAdd.create_widgets(self.__widgets)

    def __generate_operation(self):
        GraphAdd.current_scene = 'opts'
        file = open(self.__dir + 'opts.json', 'r', encoding='utf-8')
        data = json.loads(file.read())
        self.__opts = {}
        for opt_dic in data:
            temp = Opt(0, '', '')
            temp.from_dic(opt_dic)
            self.__opts[temp.name] = temp
        GraphAdd.create_opts(self.__opts)

    def __generate_ocr(self):
        GraphAdd.current_scene = 'ocrs'
        file = open(self.__dir + 'ocrs.json', 'r', encoding='utf-8')
        data = json.loads(file.read())
        self.__ocrs = []
        for ocr_dic in data:
            temp = OCRTex(0, '', [])
            temp.from_dic(ocr_dic)
            self.__ocrs.append(temp)
        GraphAdd.create_ocrs(self.__ocrs)
        for ocr in self.__ocrs:
            for sim in ocr.similar:
                GraphAdd.create_ocr_ocr(ocr, sim)
        return

    def __generate_cnt(self):
        scenes = os.listdir(self.__dir)
        cnt_seq = []
        scene_names = []
        for scene in scenes:
            if scene not in ['widgets.json', 'opts.json', 'ocrs.json']:
                scene_names.append(scene)
                file = open(self.__dir + scene, 'r', encoding='utf-8')
                data = json.loads(file.read())
                cnts = []
                for cnt_dic in data:
                    temp = Content(0, '', '', [], None, None, None, None)
                    temp.from_dic(cnt_dic)
                    cnts.append(temp)
                cnt_seq.append(cnts)

        deduplicate = MessageCompare()
        for i in range(0, len(cnt_seq)):
            GraphAdd.current_scene=scene_names[i]
            seq = cnt_seq[i]
            last = None
            for c in seq:
                same, similar = deduplicate.get_similar_cnts(c)
                next = None
                if same is None:
                    GraphAdd.add_new_content(c)
                    for sim in similar:
                        GraphAdd.create_cnt_sim_cnt(c, sim)
                    next = c
                else:
                    self.__update_cnt(c, same)
                    next = same

                if last is not None:
                    GraphAdd.create_cnt_next_cnt(last, next)
                else:
                    GraphAdd.tag_cnt_head(next)

                last = next
            GraphAdd.tag_cnt_tail(last)
        return

    def __update_cnt(self, new_cnt, original_cnt):
        if new_cnt.widget is None or new_cnt.opt is None or new_cnt.ocr is None:
            print(new_cnt.to_dic())
        if original_cnt.opt is None or original_cnt.opt.id != new_cnt.opt.id:
            GraphAdd.create_cnt_opt(original_cnt, new_cnt.opt)
        if original_cnt.widget is None or original_cnt.widget.id != new_cnt.widget.id:
            GraphAdd.create_cnt_wdg(original_cnt, new_cnt.widget)
        if original_cnt.ocr is None or original_cnt.ocr.id != new_cnt.ocr.id:
            GraphAdd.create_cnt_ocr(original_cnt, new_cnt.ocr)
