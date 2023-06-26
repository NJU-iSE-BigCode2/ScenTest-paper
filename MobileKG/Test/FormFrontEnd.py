import os
import json


def create_dir(path):
    if os.path.exists(path):
        return

    os.mkdir(path)
    return



class FormFeatureExtract:
    def __init__(self, apps):
        self.apps = apps
        return

    def execute(self):
        reports = []
        for app in self.apps:
            path = '../Data/Analyze/' + app
            scene = os.listdir(path)
            for s in scene:
                report = {
                    "app": app,
                    "scene": scene,
                    "data": self.generate_scene(app, s)
                }
                reports.append(report)

        create_dir('front_end')
        file = open('front_end/FeatureExtract.json', 'w', encoding='utf-8')
        file.write(json.dumps(reports, ensure_ascii=False))
        file.close()
        return

    def generate_scene(self, app, scene):
        result = []
        result.append(self.get_text(app, scene))
        files = os.listdir('../Data/Analyze/' + app + '/' + scene)
        for file in files:
            if os.path.isdir('../Data/Analyze/' + app + '/' + scene + '/' + file):
                continue
            elif file == 'part.json':
                continue

            result.append(self.get_pic(app, scene, file))
        return result

    def get_text(self, app, scene):
        split_contents = []
        path = '../Data/Original/' + app + '/' + scene + '/operation.txt'
        file = open(path, 'r', encoding='utf-8')
        line = file.readline()
        while line is not None and len(line) > 0:
            temp = {
                "origin": line,
                "type": 'origin'
            }
            split_contents.append(temp)
            line = file.readline()
        file.close()

        path = '../Data/Analyze/' + app + '/' + scene + '/part.json'
        parts = json.loads(open(path, 'r', encoding='utf-8').read())
        for i in range(0, len(split_contents)):
            item = split_contents[i]
            item["words"] = parts[i]
            item["str"] = parts[i]

        return {
            "id": scene + '-测试报告',
            "type": 'text',
            "split_contents": split_contents,
            "state": 'waiting',
            "steps": []
        }

    def get_pic(self, app, scene, pic):
        pic_name = pic[0: len(pic) - 4]
        component_boxes = []
        component_outputs = []
        path = '../Data/Analyze/' + app + '/' + scene + '/' + pic_name + '/component/' + pic_name + '.json'
        components = json.loads(open(path, 'r', encoding='utf-8').read())['components']
        for com in components:
            component_boxes.append(
                {
                    "x": com['x1'],
                    "y": com['y1'],
                    "width": com['x2'] - com['x1'],
                    "height": com['y2'] - com['y1']
                }
            )
            component_outputs.append(
                '(' + str(com['x1']) + ", " + str(com['y1']) + ", " + str(com['x2']) + ", " + str(com['y2']) + ")")

        ocr_boxes = []
        ocr_outputs = []
        path = '../Data/Analyze/' + app + '/' + scene + '/' + pic_name + '/ocr/' + pic_name + '.json'
        ocrs = json.loads(open(path, 'r', encoding='utf-8').read())['words_result']
        for ocr in ocrs:
            ocr_boxes.append(
                {
                    "x": ocr['location']['left'],
                    "y": ocr['location']['top'],
                    "width": ocr['location']['width'],
                    "height": ocr['location']['height']
                }
            )
            ocr_outputs.append(
                ocr['words'] + ' (' + str(ocr['location']['left']) + ", " + str(ocr['location']['top']) + ", " + str(
                    ocr['location']['left'] + ocr['location']['width']) + ", " + str(
                    ocr['location']['top'] + ocr['location']['height']) + ")")

        return {
            "id": scene + '-' + pic,
            "type": 'pics',
            "steps": [pics[scene + '-' + pic], pics[scene + '-' + pic], pics[scene + '-' + pic]],
            "state": 'waiting',
            "component_bbox": {
                "id": 'COM-' + scene + '-' + pic,
                "src": pics[scene + '-' + pic],
                "boxes": component_boxes,
                "outputs": [component_outputs]
            },
            "ocr_bbox": {
                "id": 'OCR-' + scene + '-' + pic,
                "src": pics[scene + '-' + pic],
                "boxes": ocr_boxes,
                "outputs": [ocr_outputs]
            }
        }


class FormRelationExtract:
    def __init__(self, function_point, apps):
        self.__function_point = function_point
        self.__apps = apps
        return

    def execute(self):
        reports = []
        for app in self.__apps:
            scenes = os.listdir('../Data/Original/' + app + '/')
            for s in scenes:
                reports.append(self.generate_scene(app, s))

        create_dir('front_end')
        file = open('front_end/RelationExtract.json', 'w', encoding='utf-8')
        file.write(json.dumps(reports, ensure_ascii=False))
        file.close()
        return

    def generate_scene(self, app, scene):
        origin_texts = []
        origin_text_file = open('../Data/Original/' + app + '/' + scene + '/operation.txt', 'r', encoding='utf-8')
        line = origin_text_file.readline()
        while line is not None and len(line) > 0:
            origin_texts.append(line)
            line = origin_text_file.readline()

        split_texts = json.loads(
            open('../Data/Analyze/' + app + '/' + scene + '/part.json', 'r', encoding='utf-8').read())

        data = []
        path = '../Data/Analyze/' + app + '/' + scene + '/'
        files = os.listdir(path)
        for f in files:
            if f == 'part.json':
                continue
            elif os.path.isdir(path + f):
                continue
            data.append(self.generate_pic(app, scene, f, origin_texts, split_texts))

        return {
            "app": app,
            "scene": scene,
            "data": data
        }

    def generate_pic(self, app, scene, pic, origin_texts, split_texts):
        pic_name = pic[0:len(pic) - 4]
        num = int(pic_name) - 1
        origin_text = origin_texts[num]
        split_text = split_texts[num]
        result_text = split_texts[num]

        content = json.loads(
            open('../Data/Result/' + self.__function_point + '/' + scene + '.json', 'r', encoding='utf-8').read())
        step = content[num]
        ocr_text = step['ocr']['name']
        ocr_bounding = None

        ocr_boxes = []
        ocr_outputs = []
        path = '../Data/Analyze/' + app + '/' + scene + '/' + pic_name + '/ocr/' + pic_name + '.json'
        ocrs = json.loads(open(path, 'r', encoding='utf-8').read())['words_result']
        for ocr in ocrs:
            box = {
                "x": ocr['location']['left'],
                "y": ocr['location']['top'],
                "width": ocr['location']['width'],
                "height": ocr['location']['height']
            }
            ocr_boxes.append(box)
            ocr_outputs.append(
                ocr['words'] + ' (' + str(ocr['location']['left']) + ", " + str(ocr['location']['top']) + ", " + str(
                    ocr['location']['left'] + ocr['location']['width']) + ", " + str(
                    ocr['location']['top'] + ocr['location']['height']) + ")")

            if ocr['words'] == ocr_text:
                ocr_bounding = box

        component_boxes = []
        component_outputs = []
        path = '../Data/Analyze/' + app + '/' + scene + '/' + pic_name + '/component/' + pic_name + '.json'
        components = json.loads(open(path, 'r', encoding='utf-8').read())['components']
        square, horizontal, vertical, center = 0, 0, 0, 0
        com_bounding = None
        for com in components:
            box = {
                "x": com['x1'],
                "y": com['y1'],
                "width": com['x2'] - com['x1'],
                "height": com['y2'] - com['y1']
            }
            component_boxes.append(box)
            component_outputs.append(
                '(' + str(com['x1']) + ", " + str(com['y1']) + ", " + str(com['x2']) + ", " + str(com['y2']) + ")")

            s, h, v, c = self.find_relevant(
                com['x1'], com['y1'], com['x2'], com['y2'],
                ocr_bounding['x'], ocr_bounding['y'],
                ocr_bounding['x'] + ocr_bounding['width'],
                ocr_bounding['y'] + ocr_bounding['height']
            )
            if s > square:
                square, horizontal, vertical, center = s, h, v, c
                com_bounding = box

        com_bounding_text = '(' + str(com_bounding['x']) + ', ' + str(com_bounding['y']) + ', ' + str(
            com_bounding['x'] + com_bounding['width']) + ', ' + str(com_bounding['y'] + com_bounding['height']) + ')'
        result = [["操作：" + step['opt']['name']], ["概念：" + step['name']], ["OCR文本：" + step['ocr']['name']],
                  ["控件：" + com_bounding_text],
                  ["控件类型：" + step['widget']['english']]]

        return {
            "id": scene + '-' + pic,
            "origin_text": origin_text,
            "split_text": split_text,
            "result_text": result_text,
            "type": 'pics',
            "steps": [pics[scene + '-' + pic], pics[scene + '-' + pic], pics[scene + '-' + pic]],
            "state": 'waiting',
            "search": [ocr_outputs, component_outputs],
            "result": result,
            "component_bbox": {
                "id": "COM-" + scene + '-' + pic_name,
                "src": pics[scene + '-' + pic],
                "boxes": component_boxes,
                "stopped": com_bounding
            },
            "ocr_bbox": {
                "id": 'OCR-' + scene + '-' + pic_name,
                "src": pics[scene + '-' + pic],
                "boxes": ocr_boxes,
                "stopped": ocr_bounding
            }
        }

    def find_relevant(self, x1, y1, x2, y2, x3, y3, x4, y4):
        class rect:
            def __init__(self, x1, y1, x2, y2):
                self.x1 = x1
                self.x2 = x2
                self.y1 = y1
                self.y2 = y2
                return

        left = None
        right = None
        square = 0
        if x1 <= x3:
            left = rect(x1, y1, x2, y2)
            right = rect(x3, y3, x4, y4)
        else:
            right = rect(x1, y1, x2, y2)
            left = rect(x3, y3, x4, y4)

        if left.x2 < right.x1:
            square = 0
        elif left.y2 < right.y1 or left.y1 > right.y2:
            square = 0
        else:
            x_lu = max(left.x1, right.x1)
            y_lu = max(left.y1, right.y1)
            x_rd = min(left.x2, right.x2)
            y_rd = min(left.y2, right.y2)
            square = (x_rd - x_lu) * (y_rd - y_lu)

        return square, min(abs(x3 - x2), abs(x1 - x4)), min(abs(y3 - y2), abs(y1 - y4)), pow(
            pow(x3 + x4 - x1 - x2, 2) + pow(y3 + y4 - y1 - y2, 2), 0.5) / 2


class FormGenerateGraph:
    def __init__(self, apps, function_point):
        self.__apps = apps
        self.__function_point = function_point
        return

    def execute(self):
        reports = []
        for app in self.__apps:
            scenes = os.listdir('../Data/Original/' + app)
            for s in scenes:
                reports.append(self.generate_scene(app, s))

        create_dir('front_end')
        file = open('front_end/GenerateGraph.json', 'w', encoding='utf-8')
        file.write(json.dumps(reports, ensure_ascii=False))
        file.close()
        return

    def generate_scene(self, app, scene):
        result = json.loads(
            open('../Data/Result/' + self.__function_point + '/' + scene + '.json', 'r', encoding='utf-8').read())
        data = []
        for i in range(0, len(result)):
            data.append({
                "step": i + 1,
                "opt": result[i]['opt']['name'],
                "cnt": result[i]['name'],
                "ocr": result[i]['ocr']['name'],
                "wid": result[i]['widget']['english']
            })

        create_records = json.loads(open('../Test/front_end/GraphAddRecord.json', 'r', encoding='utf-8').read())
        opts = []
        commands = []
        if scene[len(app) + 1:] == '01' and app == self.__apps[0]:
            for o in create_records['ocrs']:
                opts.append(o)
                commands.append([o])
            for o in create_records['widgets']:
                opts.append(o)
                commands.append([o])
            for o in create_records['opts']:
                opts.append(o)
                commands.append([o])
        for o in create_records[scene + '.json']:
            opts.append(o)
            commands.append([o])

        return {
            "app": app,
            "scene": scene,
            "data": data,
            "state": 'waiting',
            "type": 'pics',
            "opts": [opts],
            "commands": commands
        }


class IntelligentSearch:
    def __init__(self, app, scene, pic):
        self.__app = app
        self.__scene = scene
        self.__pic = pic
        return

    def execute(self):
        return

    def __get_origin_pic(self):
        return

    def __get_component_pic(self):
        return

    def __get_ocr_pic(self):
        return

    def __get_layout_pic(self):
        return

    def __get_result(self):
        return

class FormView:
    def __init__(self,app,scene):
        self.app=app
        self.scene=scene
        return

    def execute(self):
        feature_file=json.loads(open('front_end/FeatureExtract.json','r',encoding='utf-8').read())
        relation_file=json.loads(open('front_end/RelationExtract.json','r',encoding='utf-8').read())
        origin_part={
            'text':'',
            'pics':[]
        }
        feature_part={
            'text':'',
            'pics':[]
        }
        relation_part={
            'contents':[]
        }
        for feature in feature_file:
            for step in feature['data']:
                if self.app+'-'+self.scene+'-' in step['id']:
                    if '测试报告' in step['id']:
                        for item in step['split_contents']:
                            origin_part['text']=origin_part['text']+item['origin']
                            feature_part['text']=feature_part['text']+item['words'][0]+' '+item['words'][1]+'\n'
                    else:
                        origin_part['pics'].append({
                            'name':step['id'][len(self.app)+len(self.scene)+2:],
                            'url':pics[step['id']]
                        })
                        feature_part['pics'].append({
                            'name': step['id'][len(self.app) + len(self.scene) + 2:],
                            'url': pics['feature-'+step['id']]
                        })

        for relation in relation_file:
            if relation['scene']==self.app+'-'+self.scene:
                for step in relation['data']:
                    relation_part['contents'].append({
                        "name":step['id'],
                        "opt":step['result'][0][0],
                        "cnt":step['result'][1][0],
                        "wid":step['result'][4][0],
                        "ocr":step['result'][2][0],
                        "loc":step['result'][3][0]
                    })

        result={
            'origin':origin_part,
            'feature':feature_part,
            'relation':relation_part
        }
        create_dir('front_end')
        file = open('front_end/View.json', 'w', encoding='utf-8')
        file.write(json.dumps(result, ensure_ascii=False))
        file.close()

        return


pics = {
    'alipay-01-01.jpg': 'https://s2.loli.net/2022/03/19/VKFpm53LNRckCWz.jpg',
    'alipay-01-02.jpg': 'https://s2.loli.net/2022/03/19/go3ZqMTWCdKNGYe.jpg',
    'alipay-01-03.jpg': 'https://s2.loli.net/2022/03/19/mwC2UFEnoVLBjvu.jpg',
    'alipay-01-04.jpg': 'https://s2.loli.net/2022/03/19/2fwrLT7K64ncgil.jpg',
    'alipay-01-05.jpg': 'https://s2.loli.net/2022/03/19/Yz7SaVP1NA2dBfu.jpg',
    'alipay-01-06.jpg': 'https://s2.loli.net/2022/03/19/nmiWdTN6P4O9Bkf.jpg',
    'alipay-01-07.jpg': 'https://s2.loli.net/2022/03/19/PaOUgMrXyiD4fkA.jpg',
    'alipay-01-08.jpg': 'https://s2.loli.net/2022/03/19/os15g78rbZDPRnB.jpg',
    'alipay-02-01.jpg': 'https://s2.loli.net/2022/03/19/VKFpm53LNRckCWz.jpg',
    'alipay-02-02.jpg': 'https://s2.loli.net/2022/03/19/go3ZqMTWCdKNGYe.jpg',
    'alipay-02-03.jpg': 'https://s2.loli.net/2022/03/19/9c2Vxr8Q6o35XGa.jpg',
    'alipay-02-04.jpg': 'https://s2.loli.net/2022/03/19/IV6X7AmnLU3sZfj.jpg',
    'PTEdanci-01-01.jpg': 'https://s2.loli.net/2022/03/19/EzGXjQq7Sifpt5D.jpg',
    'PTEdanci-01-02.jpg': 'https://s2.loli.net/2022/03/19/crCWVhs9LOvjzpZ.jpg',
    'PTEdanci-01-03.jpg': 'https://s2.loli.net/2022/03/19/UEPcqStnvmjaw4i.jpg',
    'PTEdanci-01-04.jpg': 'https://s2.loli.net/2022/03/19/4WAB1j9DTs3ItUE.jpg',
    'PTEdanci-01-05.jpg': 'https://s2.loli.net/2022/03/19/5iqPyHZrXwVbBEM.jpg',
    'PTEdanci-01-06.jpg': 'https://s2.loli.net/2022/03/19/xl7RPcmG6uazFgT.jpg',
    'PTEdanci-01-07.jpg': 'https://s2.loli.net/2022/03/19/wzEsTBPgkYWXZ5F.jpg',
    'PTEdanci-01-08.jpg': 'https://s2.loli.net/2022/03/19/qRBco83JAeZiaXO.jpg',
    'feature-alipay-02-01.jpg':'https://s2.loli.net/2022/03/28/AJXgY6FxrcOoeCj.jpg',
    'feature-alipay-02-02.jpg': 'https://s2.loli.net/2022/03/28/P3iCRUjI5WGpov6.jpg',
    'feature-alipay-02-03.jpg': 'https://s2.loli.net/2022/03/28/8rqwXQiH3WaRd6t.jpg',
    'feature-alipay-02-04.jpg': 'https://s2.loli.net/2022/03/28/PqrLhnod7mHNzpe.jpg',
}

# fre = FormFeatureExtract(['alipay','PTEdanci'])
# fre.execute()
#
# fre = FormRelationExtract('20220319222421', ['alipay','PTEdanci'])
# fre.execute()

# fre = FormGenerateGraph(['alipay','PTEdanci'], '20220319222421')
# fre.execute()

fv=FormView('alipay','02')
fv.execute()
