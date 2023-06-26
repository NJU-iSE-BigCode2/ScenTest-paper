from MobileKG.PicAnalysis.component_algorithm.canny import Canny
from MobileKG.PicAnalysis.component_algorithm.uied_component import ip_region_proposal
from MobileKG.PicAnalysis.config.Config import Config
from MobileKG.PicAnalysis.config.Config_enum import Config_enum
from MobileKG.PicAnalysis.merge_algorithm.uied_merge import Uied_merge
from MobileKG.PicAnalysis.text_algorithm.baidu_ocr import Baidu_ocr
from MobileKG.PicAnalysis.merge_algorithm.canny_ocr_merge import Canny_ocr_merge

config = Config()
option = Config_enum()


def get_component_algorithm(C_in=None):
    global config
    if C_in is not None:
        config = C_in
    if config.COMPONENT_OPTION == option.CANNY_COMPONENT:
        return Canny.run
    if config.COMPONENT_OPTION == option.UIED_COMPONENT:
        return ip_region_proposal.run


def get_text_algorithm(C_in=None):
    global config
    if C_in is not None:
        config = C_in
    if config.TEXT_OPTION == option.BAIDU_OCR:
        return Baidu_ocr.run


def get_merge_algorithm(C_in=None):
    global config
    if C_in is not None:
        config = C_in
    if config.MERGE_OPTION == option.CANNY_OCR_MERGE:
        return Canny_ocr_merge.run
    if config.MERGE_OPTION == option.UIED_MERGE:
        return Uied_merge.run
