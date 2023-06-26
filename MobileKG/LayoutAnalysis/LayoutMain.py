from MobileKG.LayoutAnalysis.LayoutExtract import generate_layout_json
from MobileKG.SearchKG.po.Layout import Layout
from MobileKG.LayoutAnalysis.Sift import comparewithImage
import json

def match(layout: Layout, picture, split_dic):
    h, w = picture.shape
    result_x1 = 0
    result_x2 = 0
    result_y1 = 0
    result_y2 = 0
    rate_x = 0
    rate_y = 0
    result_rate = 0
    for part in split_dic:
        y1 = part['top']
        y2 = part['bottom']
        x1 = 0
        x2 = w
        part_picture = picture[y1:y2, x1:x2]
        similar_rate = 0
        similar_sample = None
        for sample in layout.sample:
            try:
                temp_similar_rate = comparewithImage(sample['sample'], part_picture)
            except Exception as e:
                temp_similar_rate = 0
            if temp_similar_rate > similar_rate:
                similar_rate = temp_similar_rate
                similar_sample = sample
        # similar_rate = comparewithImage(layout.sample, part_picture)
        if similar_rate > result_rate:
            result_rate = similar_rate
            result_x1 = x1
            result_x2 = x2
            result_y1 = y1
            result_y2 = y2
            rate_x = similar_sample['x']
            rate_y = similar_sample['y']

    return result_x1, result_y1, result_x2 - result_x1, result_y2 - result_y1, rate_x, rate_y

def split(pic_path):
    return json.loads(generate_layout_json(pic_path))
