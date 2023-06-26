from MobileKG.GenerateKG.po.Widget import Widget
from MobileKG.GenerateKG.po.Content import Content
from MobileKG.GenerateKG.po.Opt import Opt
import pandas as pd
import os
import json
from MobileKG.Neo4j.GraphSearch import GraphSearch
import datetime
from MobileKG.GenerateKG.operation.TextPicBound import TextPicBound

class RelationExtract:
    def __init__(self, dirs, ocr_sim, opt_sim, input_sim, result_path, exist_path):
        self.__dirs = dirs
        self.__ocr_sim = ocr_sim
        self.__opt_sim = opt_sim
        self.__input_sim = input_sim
        self.__result_path = result_path
        now = datetime.datetime.now()
        self.__time = now.strftime("%Y%m%d%H%M%S")
        self.__bound = None
        self.__exist_path = exist_path
        self.__cnts = self.__get_cnt_num()
        return

    def execute(self):
        widgets = self.__create_widget()
        opts = self.__create_operation()
        self.__bound = TextPicBound(opts, widgets, self.__opt_sim, self.__input_sim, self.__ocr_sim, self.__result_path,
                                    self.__time, self.__exist_path)
        self.__create_content()
        self.__save_opts()
        self.__save_widgets()
        return

    def __create_widget(self):
        widgets = {}
        if self.__exist_path is not None:
            file = json.loads(open(self.__exist_path + 'widgets.json', 'r', encoding='utf-8').read())
            for dic in file:
                temp = Widget(0, '', '')
                temp.from_dic(dic)
                widgets[temp.english] = temp
            return widgets
        else:
            config = pd.read_csv('../Config/WidgetConfig.csv')
            nums = config.shape[0]

            for i in range(0, nums):
                temp = Widget(config['id'][i], config['name'][i], config['english'][i])
                widgets[temp.english] = temp
            return widgets

    def __create_operation(self):
        operations = {}
        if self.__exist_path is not None:
            file = json.loads(open(self.__exist_path + 'opts.json', 'r', encoding='utf-8').read())
            for dic in file:
                temp = Opt(0, '', '')
                temp.from_dic(dic)
                operations[temp.name] = temp
            return operations
        else:
            config = pd.read_csv('../Config/OperationConfig.csv')
            nums = config.shape[0]

            for i in range(0, nums):
                temp = Opt(config['id'][i], config['name'][i], config['english'][i])
                operations[temp.name] = temp
            return operations

    def __create_content(self):
        for cnt_dir in self.__dirs:
            relation = self.__analyze_scene(cnt_dir)
            self.__save_relation(relation, cnt_dir)
        return

    def __analyze_scene(self, scene):
        steps_size = int(len(os.listdir(scene)) / 2)
        file = open(scene + '/part.json', 'r', encoding='utf-8')
        texts = json.loads(file.read())
        file.close()
        contents = []
        for i in range(0, steps_size):
            pic_dir_name = str(i + 1).zfill(2)
            contents.append(self.__analyze_step(scene + '/' + pic_dir_name, texts[i], pic_dir_name))
        return contents

    def __analyze_step(self, scene_pic, scene_txt, step):
        opt = self.__bound.get_operation(scene_txt)
        cnt = self.__bound.get_cnt(scene_txt)
        layout = self.__bound.get_layout()
        cnt_ocr_match, ocr = self.__bound.get_ocr(scene_pic, cnt, step)
        widget = self.__bound.get_widget(scene_pic, step, cnt_ocr_match, opt)
        content = Content(self.__cnts + 1, cnt, '', [], opt, widget, layout, ocr)
        self.__cnts = self.__cnts + 1

        def is_valid(type, o):
            if o is None:
                print('!!![' + type + ' is None] pic at:' + scene_pic)

        is_valid('opt', opt)
        is_valid('cnt', cnt)
        is_valid('layout', layout)
        is_valid('cnt_ocr_match', cnt_ocr_match)
        is_valid('ocr', ocr)
        is_valid('widget', widget)
        return content

    def __save_relation(self, contents, path):
        index = 0
        for i in range(0, len(path)):
            if path[len(path) - 1 - i] == '/':
                index = i
                break
        dir_path = self.__result_path + self.__time
        if self.__exist_path is not None:
            dir_path = self.__exist_path[0:len(self.__exist_path) - 1]
        self.__create_dir(dir_path)
        path = dir_path + '/' + path[len(path) - 1 - index + 1:] + '.json'
        result = []
        for cnt in contents:
            result.append(cnt.to_dic())
        file = open(path, 'w', encoding='utf-8')
        file.write(json.dumps(result, ensure_ascii=False))
        file.close()

    def __save_opts(self):
        dir_path = self.__result_path + self.__time
        if self.__exist_path is not None:
            dir_path = self.__exist_path[0:len(self.__exist_path) - 1]
        self.__create_dir(dir_path)
        opts = []
        bound_opts = self.__bound.get_opts()
        for o in bound_opts:
            opts.append(bound_opts[o].to_dic())
        file = open(dir_path + '/opts.json', 'w', encoding='utf-8')
        file.write(json.dumps(opts, ensure_ascii=False))
        file.close()
        return

    def __save_widgets(self):
        dir_path = self.__result_path + self.__time
        if self.__exist_path is not None:
            dir_path = self.__exist_path[0:len(self.__exist_path) - 1]
        self.__create_dir(dir_path)
        widgets = []
        bound_widgets = self.__bound.get_widgets()
        for w in bound_widgets:
            widgets.append(bound_widgets[w].to_dic())
        file = open(dir_path + '/widgets.json', 'w', encoding='utf-8')
        file.write(json.dumps(widgets, ensure_ascii=False))
        file.close()
        return

    def __create_dir(self, path):
        if os.path.exists(path):
            return
        os.mkdir(path)
        return

    def __get_cnt_num(self):
        result = 0
        if self.__exist_path is None:
            return result

        dirs = os.listdir(self.__exist_path)
        exceptions = ['ocrs.json', 'opts.json', 'widgets.json']
        for dir in dirs:
            if dir in exceptions:
                continue
            content = json.loads(open(self.__exist_path + dir, 'r', encoding='utf-8').read())
            for c in content:
                if int(c['id']) > result:
                    result = int(c['id'])

        return result + 1
