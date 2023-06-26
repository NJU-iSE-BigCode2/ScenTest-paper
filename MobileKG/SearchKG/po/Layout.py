import cv2
from MobileKG.Config.RunConfig import graph_type


class Layout:
    layout_pics_path = '../Config/LayoutPics/' + graph_type + '/'

    def __init__(self, layout_dic):
        self.cnt = layout_dic['cnt']
        self.opt = layout_dic['opt']
        self.widget = layout_dic['widget']
        self.ocr = layout_dic['ocr']
        samples = []
        for sample in layout_dic['samples']:
            samples.append({
                "sample": cv2.imread(Layout.layout_pics_path + sample['sample'], 0),
                "x": sample['x'],
                "y": sample['y']
            })
        # self.sample = cv2.imread(Layout.layout_pics_path + layout_dic['sample'], 0)
        self.sample = samples
        # self.x = layout_dic['x']
        # self.y = layout_dic['y']
        return

    def to_dic(self):
        return
