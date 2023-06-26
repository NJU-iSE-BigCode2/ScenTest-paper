from MobileKG.GenerateKG.po.Opt import Opt
from MobileKG.GenerateKG.po.Widget import Widget
from MobileKG.GenerateKG.po.Layout import Layout
from MobileKG.GenerateKG.po.OCRTex import OCRTex


class Node:
    def __init__(self, id, name, english, similar, opt, widget, layout, ocr):
        self.id: int = id
        self.name: str = name
        self.english: str = english
        self.similar: list = similar
        self.opt: Opt = opt
        self.widget: Widget = widget
        self.layout: Layout = layout
        self.ocr: list[OCRTex] = ocr
        self.state: str = 'M'

    def get_str(self):
        return '{id:' + str(self.id) + ',name:"' + self.name + '",english:"' + self.english + '"}'
