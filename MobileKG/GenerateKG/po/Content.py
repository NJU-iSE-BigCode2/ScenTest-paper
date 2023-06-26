from MobileKG.GenerateKG.po.Opt import Opt
from MobileKG.GenerateKG.po.Widget import Widget
from MobileKG.GenerateKG.po.Layout import Layout
from MobileKG.GenerateKG.po.OCRTex import OCRTex


class Content:
    def __init__(self, id, name, english, similar, opt, widget, layout, ocr):
        self.id: int = id
        self.name: str = name
        self.english: str = english
        self.similar: list = similar
        self.opt: Opt = opt
        self.widget: Widget = widget
        self.layout: Layout = layout
        self.ocr: OCRTex = ocr

    def get_str(self):
        return '{id:' + str(self.id) + ',name:"' + self.name + '",english:"' + self.english + '"}'

    def to_dic(self):
        result = {
            "id": str(self.id),
            "name": self.name,
            "english": self.english,
            "similar": [],
            "opt": '',
            "widget": '',
            "layout": '',
            "ocr": ''
        }
        for sim in self.similar:
            sim.similar = []
            result['similar'].append(sim.to_dic())
        if self.opt is not None:
            result['opt'] = self.opt.to_dic()
        if self.widget is not None:
            result['widget'] = self.widget.to_dic()
        if self.layout is not None:
            result['layout'] = ''
        if self.ocr is not None:
            result['ocr'] = self.ocr.to_dic()
        return result

    def from_dic(self, dic):
        self.id = int(dic["id"])
        self.name = dic["name"]
        self.english = dic["english"]
        self.similar = []
        self.opt = None
        self.widget = None
        self.layout = None
        self.ocr = None
        for sim in dic['similar']:
            temp = OCRTex(0, '', [])
            temp.from_dic(sim)
            self.similar.append(temp)
        if dic['opt'] != '':
            temp = Opt(-1, '', '')
            temp.from_dic(dic['opt'])
            self.opt = temp
        if dic['widget'] != '':
            temp = Widget(-1, '', '')
            temp.from_dic(dic['widget'])
            self.widget = temp
        if dic['layout'] != '':
            self.layout = None
        if dic['ocr'] != '':
            temp = OCRTex(-1, '', [])
            temp.from_dic(dic['ocr'])
            self.ocr = temp
