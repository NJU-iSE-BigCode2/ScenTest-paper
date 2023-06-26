import numpy as np


class Bbox:
    def __init__(self, col_min, row_min, col_max, row_max, category=None, ocr_text=''):
        self.col_min = col_min
        self.row_min = row_min
        self.col_max = col_max
        self.row_max = row_max
        self.category = category
        self.ocr_text = ocr_text

        self.width = col_max - col_min
        self.height = row_max - row_min
        self.area = self.width * self.height

    def get_coordinates(self):
        return self.col_min, self.row_min, self.col_max, self.row_max

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_area(self):
        return self.area

    def get_ocr_text(self):
        return self.ocr_text

    def calc_intersection_area(self, bbox_b):
        a = self.get_coordinates()
        b = bbox_b.get_coordinates()
        col_min_s = max(a[0], b[0])
        row_min_s = max(a[1], b[1])
        col_max_s = min(a[2], b[2])
        row_max_s = min(a[3], b[3])
        w = np.maximum(0, col_max_s - col_min_s)
        h = np.maximum(0, row_max_s - row_min_s)
        inter = w * h
        return inter

    def bbox_merge(self, bbox_b):
        '''
        Merge two intersected bboxes
        '''
        col_min_a, row_min_a, col_max_a, row_max_a = self.get_coordinates()
        col_min_b, row_min_b, col_max_b, row_max_b = bbox_b.get_coordinates()
        col_min = min(col_min_a, col_min_b)
        col_max = max(col_max_a, col_max_b)
        row_min = min(row_min_a, row_min_b)
        row_max = max(row_max_a, row_max_b)
        new_bbox = Bbox(col_min, row_min, col_max, row_max)
        return new_bbox

    def bbox_merge_option(self, element_b, new_element=False, new_category=None):
        if not new_element:
            bbox = self.bbox_merge(element_b)
            self.col_max = bbox.col_max
            self.col_min = bbox.col_min
            self.row_min = bbox.row_min
            self.row_max = bbox.row_max
        else:
            bbox = self.bbox_merge(element_b)
            bbox.category = new_category
            return bbox

    def bbox_relation(self, bbox_b, bias=(0, 0)):
        '''
        Calculate the relation between two rectangles by nms
       :return: -1 : a in b
         0  : a, b are not intersected
         1  : b in a
         2  : a, b are intersected
       '''
        col_min_a, row_min_a, col_max_a, row_max_a = self.get_coordinates()
        col_min_b, row_min_b, col_max_b, row_max_b = bbox_b.get_coordinates()

        bias_col, bias_row = bias
        # get the intersected area
        col_min_s = max(col_min_a - bias_col, col_min_b - bias_col)
        row_min_s = max(row_min_a - bias_row, row_min_b - bias_row)
        col_max_s = min(col_max_a + bias_col, col_max_b + bias_col)
        row_max_s = min(row_max_a + bias_row, row_max_b + bias_row)
        w = np.maximum(0, col_max_s - col_min_s)
        h = np.maximum(0, row_max_s - row_min_s)
        inter = w * h
        area_a = (col_max_a - col_min_a) * (row_max_a - row_min_a)
        area_b = (col_max_b - col_min_b) * (row_max_b - row_min_b)
        iou = inter / (area_a + area_b - inter)
        ioa = inter / self.area
        iob = inter / bbox_b.area

        if iou == 0 and ioa == 0 and iob == 0:
            return 0

        # import lib_ip.ip_preprocessing as pre
        # org_iou, _ = pre.read_img('uied/data/input/7.jpg', 800)
        # print(iou, ioa, iob)
        # board = draw.draw_bounding_box(org_iou, [self], color=(255,0,0))
        # draw.draw_bounding_box(board, [bbox_b], color=(0,255,0), show=True)

        # contained by b
        if ioa >= 1:
            return -1
        # contains b
        if iob >= 1:
            return 1
        # not intersected with each other
        # intersected
        if iou >= 0.02 or iob > 0.2 or ioa > 0.2:
            return 2
        # if iou == 0:
        # print('ioa:%.5f; iob:%.5f; iou:%.5f' % (ioa, iob, iou))
        return 0
