from MobileKG.PicAnalysis.config.Config_enum import Config_enum

option = Config_enum()


class Config:
    def __init__(self):
        self.COMPONENT_OPTION = option.CANNY_COMPONENT
        self.TEXT_OPTION = option.BAIDU_OCR
        self.MERGE_OPTION = option.CANNY_OCR_MERGE

        self.OUTPUT_PATH = 'data/output'
        self.OUTPUT_COMPONENT_PATH = 'data/output/component'
        self.OUTPUT_OCR_PATH = 'data/output/ocr'
        self.OUTPUT_MERGE_PATH = 'data/output/merge'

        '''
            ele:min-grad: gradient threshold to produce binary map         
            ele:ffl-block: fill-flood threshold
            ele:min-ele-area: minimum area for selected elements 
            ele:merge-contained-ele: if True, merge elements contained in others
            text:max-word-inline-gap: words with smaller distance than the gap are counted as a line
            text:max-line-gap: lines with smaller distance than the gap are counted as a paragraph

            Tips:
            1. Larger *min-grad* produces fine-grained binary-map while prone to over-segment element to small pieces
            2. Smaller *min-ele-area* leaves tiny elements while prone to produce noises
            3. If not *merge-contained-ele*, the elements inside others will be recognized, while prone to produce noises
            4. The *max-word-inline-gap* and *max-line-gap* should be dependent on the input image size and resolution

            mobile: {'min-grad':4, 'ffl-block':5, 'min-ele-area':50, 'max-word-inline-gap':6, 'max-line-gap':1}
            web   : {'min-grad':3, 'ffl-block':5, 'min-ele-area':25, 'max-word-inline-gap':4, 'max-line-gap':4}
            origin:{'min-grad': 10, 'ffl-block': 5, 'min-ele-area': 50, 'merge-contained-ele': True,
                                'max-word-inline-gap': 4, 'max-line-gap': 4}
        '''

        self.UIED_key_params = {'min-grad': 3, 'ffl-block': 5, 'min-ele-area': 25, 'max-word-inline-gap': 4,
                                'max-line-gap': 4, 'merge-contained-ele': False}

    def update_path(self, output_path, component_path, ocr_path, merge_path):
        self.OUTPUT_PATH = output_path
        self.OUTPUT_COMPONENT_PATH = component_path
        self.OUTPUT_OCR_PATH = ocr_path
        self.OUTPUT_MERGE_PATH = merge_path
