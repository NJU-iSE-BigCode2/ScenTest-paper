import json
import os
import shutil

import cv2 as cv


def draw_rectangle_show_save(src, bboxs, output_path, show=False, show_title='image', line=3, color=(0, 0, 255)):
    image = src.copy()
    for bbox in bboxs:
        x1, y1, x2, y2 = bbox.get_coordinates()
        cv.rectangle(image, (x1, y1), (x2, y2), color, line)
    cv.imwrite(output_path, image)
    if show:
        cv.imshow(show_title, image)
        cv.waitKey(0)


def save_bboxs_as_json(bboxs, save_path):
    res = {'components': []}
    for b in bboxs:
        x1, y1, x2, y2 = b.get_coordinates()
        category = b.category
        res['components'].append({'category': category, 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2})
    json.dump(res, open(save_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)


def clean_dir(dir_path):
    for i in os.listdir(dir_path):
        file_data = dir_path + "\\" + i
        if os.path.isfile(file_data) == True:
            os.remove(file_data)
        else:
            shutil.rmtree(file_data)
