import time
import cv2 as cv
from MobileKG.PicAnalysis.config.Config import Config
import numpy as np


def reclassify_text_by_ocr(compos, texts):
    compos_new = []
    for i, compo in enumerate(compos):
        # broad = draw_bounding_box(org, [compo], show=True)
        new_compo = None
        text_area = 0
        for j, text in enumerate(texts):
            # get the intersected area
            inter = compo.calc_intersection_area(text)
            if inter == 0:
                continue

            # calculate IoU
            ioa = inter / compo.area
            iob = inter / text.area
            iou = inter / (compo.area + text.area - inter)

            # print('ioa:%.3f, iob:%.3f, iou:%.3f' %(ioa, iob, iou))
            # draw_bounding_box(broad, [text], color=(255,0,0), line=2, show=True)

            # text area
            if ioa >= 0.68 or iou > 0.55:
                new_compo = compo.bbox_merge_option(text, new_element=True, new_category='TEXT')
                texts[j] = new_compo
                break
            text_area += inter

        # print("Text area ratio:%.3f" % (text_area / compo.area))
        if new_compo is not None:
            compos_new.append(new_compo)
        elif text_area / compo.area > 0.4:
            compo.category = 'TEXT'
            compos_new.append(compo)
        else:
            compos_new.append(compo)
    return compos_new


def merge_intersected_compos(compos, max_gap=(0, 0), merge_class=None):
    changed = False
    new_compos = []
    for i in range(len(compos)):
        if merge_class is not None and compos[i].category != merge_class:
            new_compos.append(compos[i])
            continue
        merged = False
        cur_compo = compos[i]
        for j in range(len(new_compos)):
            if merge_class is not None and new_compos[j].category != merge_class:
                continue
            relation = cur_compo.bbox_relation(new_compos[j], max_gap)
            if relation != 0:
                new_compos[j].bbox_merge_option(cur_compo)
                cur_compo = new_compos[j]
                merged = True
                changed = True
                # break
        if not merged:
            new_compos.append(compos[i])

    if not changed:
        return compos
    else:
        return merge_intersected_compos(new_compos, max_gap, merge_class)


def rm_compos_in_text(compos):
    mark = np.zeros(len(compos))
    for i, c1 in enumerate(compos):
        if c1.category != 'Text':
            continue
        for j, c2 in enumerate(compos):
            if c2.category == 'Text' or mark[j] != 0:
                continue
            if c1.bbox_relation(c2) != 0:
                c1.bbox_merge_option(c2)
                mark[j] = 1

    new_compos = []
    for i, m in enumerate(mark):
        if m == 0:
            new_compos.append(compos[i])
    return new_compos


def incorporate(C, com_bboxs, text_bboxs, show=False):
    compos_merged = reclassify_text_by_ocr(com_bboxs, text_bboxs)

    # merge words as line
    compos_merged = merge_intersected_compos(compos_merged, max_gap=(C.UIED_key_params['max-word-inline-gap'], 0),
                                             merge_class='TEXT')
    # merge lines as paragraph
    compos_merged = merge_intersected_compos(compos_merged, max_gap=(0, C.UIED_key_params['max-line-gap']),
                                             merge_class='Text')
    # clean compos intersected with paragraphs
    compos_merged = rm_compos_in_text(compos_merged)
    return compos_merged


def run(config, com_bboxs, text_bboxs, show=False):
    start = time.time()
    res = incorporate(config, com_bboxs, text_bboxs, show)
    print('Complete component extraction in {:.2f} seconds'.format(time.time() - start))
    return res
