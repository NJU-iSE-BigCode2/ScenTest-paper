import json
import os
import sys
import time
import cv2 as cv
from MobileKG.PicAnalysis.config.Config import Config
from aip import AipOcr

from MobileKG.PicAnalysis.utils.Bbox import Bbox
from MobileKG.PicAnalysis.utils.tools import draw_rectangle_show_save


def ocr(image_bytes, lang='CHN_ENG', show_char=False):
    # Use your own id and keys below.
    APP_ID = ''
    API_KEY = ''
    SECRET_KEY = ''

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    options = {
        'language-type': lang,
        'recognize_granularity': 'small' if show_char else 'big',
        'probability': 'true'
    }
    # general_res = client.general(image_bytes, options)
    acc_res = client.accurate(image_bytes, options)
    return acc_res


def deep_ocr(C, image_path, lang='CHN_ENG', prob=0.90, space_ratio=0.7):
    cache_dir = C.OUTPUT_OCR_PATH
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, '%s.json' %
                              os.path.basename(image_path)[0: os.path.basename(image_path).index(".")])
    if os.path.isfile(cache_file):
        os.remove(cache_file)
    result = ocr(open(image_path, 'rb').read(), lang)
    if 'words_result' not in result:
        print('OCR failed: %s' % str(result), file=sys.stderr)
        return []
    text_boxes = []
    for words in result['words_result']:
        texts = words['words']
        q_loc = words['location']
        left = q_loc['left']
        top = q_loc['top']
        width = q_loc['width']
        height = q_loc['height']
        text_boxes.append(Bbox(left, top, left + width, top + height, 'TEXT', texts))
    image = cv.imread(image_path)

    json.dump(result, open(cache_file, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
    draw_rectangle_show_save(image, text_boxes, C.OUTPUT_OCR_PATH + '/result.jpg')
    return text_boxes


def run(config, image_path):
    start = time.time()
    res = deep_ocr(config, image_path)
    print('Complete component extraction in {:.2f} seconds'.format(time.time() - start))
    return res


