import os
import json
from MobileKG.PicAnalysis.config.Config import *
from MobileKG.PicAnalysis.ExtractPic import ExtractPic
from MobileKG.TextAnalysis.SpeechAnalysis.ExtractText import *

class FeatureExtract:
    __dirs = []
    __original_path = '../Data/Original'
    __result_path = '../Data/Analyze'

    def __init__(self, dirs, original_path, result_path):
        if original_path is not None:
            self.__original_path = original_path

        if result_path is not None:
            self.__result_path = result_path

        if dirs is not None and len(dirs) > 0:
            self.__dirs = dirs
        else:
            self.__dirs = os.listdir(self.__original_path)

    def execute(self):
        for app in self.__dirs:
            self.__app_extraction(app)

    def __app_extraction(self, app_name):
        self.__create_dir(self.__result_path + '/' + app_name)
        scenes = os.listdir(self.__original_path + '/' + app_name)
        for scene in scenes:
            self.__scene_extraction(app_name + '/' + scene)
        return

    def __scene_extraction(self, path):
        self.__create_dir(self.__result_path + '/' + path)
        pics_path = os.listdir(self.__original_path + '/' + path)
        for pic_path in pics_path:
            self.__pic_extraction(self.__original_path + '/' + path + "/" + pic_path)
        operation_file = open(self.__original_path + '/' + path + '/operation.txt', encoding='utf-8',mode='r')
        line = operation_file.readline()
        text = []
        while line is not None and len(line) > 0:
            text.append(self.__text_extraction(line))
            line = operation_file.readline()
        operation_file.close()
        part_file = open(self.__result_path + '/' + path + '/part.json', encoding='utf-8',mode='w')
        part_file.write(json.dumps(text,ensure_ascii=False))
        return

    def __pic_extraction(self, path):
        suffix_index = -1;
        for i in range(0, len(path) - 1):
            if path[len(path) - 1 - i] == '.':
                suffix_index = len(path) - 1 - i;
                break
        pic_type = path[suffix_index:]
        if pic_type not in ['.jpg', '.png', '.jpeg']:
            return
        dir = str(path[0:suffix_index]).replace(self.__original_path, self.__result_path)
        self.__create_dir(dir)
        original_path = path
        result_path = str(path).replace(self.__original_path, self.__result_path)
        C = Config()
        C.update_path(dir, dir + '/component', dir + '/ocr', dir + '/merge')
        option = Config_enum()
        main = ExtractPic(C, option)
        main.run_widget_ext(original_path, result_path)
        return

    def __text_extraction(self, line) -> list:
        verb, object = extract_keyword(line)
        return [verb, object]

    def __create_dir(self, path):
        if os.path.exists(path):
            return

        os.mkdir(path)
        return
