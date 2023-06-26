import os
import time

import numpy as np
import cv2 as cv
from os.path import join as pjoin
from MobileKG.PicAnalysis.utils.Bbox import Bbox
from MobileKG.PicAnalysis.utils.tools import save_bboxs_as_json, draw_rectangle_show_save
from MobileKG.PicAnalysis.config.Config import Config


def canny_boundings(C, image_path, canny_sigma=0.33, dilate_count=4):
    directory = C.OUTPUT_COMPONENT_PATH
    if not os.path.exists(directory):
        os.makedirs(directory)
    image = cv.imread(image_path)
    print(image_path)
    assert image is not None, 'Wrong picture path'
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    v = np.median(gray)
    lower_threshold = int(max(0, (1 - canny_sigma) * v))
    upper_threshold = int(min(255, (1 + canny_sigma) * v))
    img_binary = cv.Canny(gray, lower_threshold, upper_threshold, -1)
    img_dilated = cv.dilate(img_binary, None, iterations=dilate_count)
    try:
        _, contours, _ = cv.findContours(img_dilated, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    except Exception as e:
        contours, _ = cv.findContours(img_dilated, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # Find bounding using contours.
    boundings = [cv.boundingRect(c) for c in contours]
    bboxs = [Bbox(b[0], b[1], b[0] + b[2], b[1] + b[3], 'COMPONENT') for b in boundings]
    name = image_path.split('/')[-1][:-4]
    save_bboxs_as_json(bboxs, os.path.join(C.OUTPUT_COMPONENT_PATH, name + '.json'))
    draw_rectangle_show_save(cv.imread(image_path), bboxs, C.OUTPUT_COMPONENT_PATH + '/result.jpg')
    return bboxs


def run(config, image_path):
    start = time.time()
    res = canny_boundings(config, image_path)
    print('Complete component extraction in {:.2f} seconds'.format(time.time() - start))
    return res
