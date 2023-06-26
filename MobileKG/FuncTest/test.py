from MobileKG.PicAnalysis.text_algorithm.baidu_ocr import Baidu_ocr
from MobileKG.PicAnalysis.ExtractPic import ExtractPic
from MobileKG.PicAnalysis.config.Config import Config, Config_enum
from MobileKG.LayoutAnalysis.LayoutMain import split
from MobileKG.SearchKG.SearchMain import next_step
from MobileKG.PicAnalysis.utils.tools import draw_rectangle_show_save
from MobileKG.PicAnalysis.utils.Bbox import Bbox

import json
import cv2
import os


def searchKG(img_path):
    config = Config()
    enum = Config_enum()
    main = ExtractPic(config, enum)

    img_path = img_path
    KG_path = img_path.replace('origin', 'KG_res')
    KG_path = KG_path.replace('jpg', 'png')
    last_cn_id = 0

    picture = cv2.imread(img_path, 0)
    split_dic = split(img_path)
    components = main.generate_widget_info(img_path)
    res = next_step(picture, split_dic, components, last_cn_id)
    print(res)
    bboxs = []
    for data in res['data']:
        bboxs.append(Bbox(data['x1'], data['y1'], data['x2'], data['y2']))
    pic = cv2.imread(img_path)
    draw_rectangle_show_save(pic, bboxs, KG_path)


searchKG('screenshot/email/origin/outlook (1).jpg')
