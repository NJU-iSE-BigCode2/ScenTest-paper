from appium import webdriver
import time
import cv2
import math

from MobileKG.FuncTest.run_command import uninstall_appium_setting, get_screenshot, uninstall_app, get_cur_activity_name, input_text
from MobileKG.FuncTest.XMLParser import XMLParser
from MobileKG.FuncTest.Context import Context
from MobileKG.PicAnalysis.config.Config import Config, Config_enum
from MobileKG.PicAnalysis.ExtractPic import ExtractPic
from MobileKG.LayoutAnalysis.LayoutMain import split
from MobileKG.SearchKG.SearchMain import next_step
from MobileKG.PicAnalysis.utils.tools import draw_rectangle_show_save
from MobileKG.PicAnalysis.utils.Bbox import Bbox
from MobileKG.FuncTest.TestNode import TestNode


class AutoTestTool:

    def __init__(self, func_name, app_package, app_activity, app_path):
        self.app_package = app_package
        self.app_name = self.app_package.split(".")[:-1]
        self.app_activity = app_activity
        self.app_path = app_path
        self.driver = None
        self.parser = XMLParser()
        self.test_context = Context()
        self.test_terminated = False
        self.config = Config()
        self.enum = Config_enum()
        self.extract_pic = ExtractPic(self.config, self.enum)
        self.operation = {"Input": self.input, "Click": self.click, "Swipe": self.swipe}
        self.func_name = func_name

    def appium_init(self):
        if self.driver is not None:
            self.appium_quit()
        desired_caps = {'browserName': '',
                        'platformName': 'Android',
                        'deviceName': 'Android Emulator',
                        'appPackage': self.app_package,
                        'appActivity': self.app_activity,
                        'noSign': 'true',
                        'app': self.app_path,
                        'newCommandTimeOut': 3000,
                        'unicodeKeyboard': 'true',
                        'resetKeyboard': 'true',
                        }
        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)
        self.driver.implicitly_wait(8)

    def click(self, x1, y1, x2, y2, content):
        try:
            self.driver.tap([(x1, y1), (x2, y2)])
            return True
        except Exception as e:
            return False

    def swipe(self, x1, y1, x2, y2, content):
        try:
            self.driver.swipe(x1, y1, x2, y2)
            return True
        except Exception as e:
            return False

    def input(self, x1, y1, x2, y2, content):
        try:
            input_text(content)
            return True
        except Exception as e:
            return False

    def default_opera(self, x1, y1, x2, y2, content):
        print("operation key error, pos:[{},{}],[{},{}], cnt:{}".format(x1, y1, x2, y2, content))

    def test_by_KG(self):
        while not self.test_terminated:
            screenshot_path = get_screenshot(self.app_name)
            KG_path = screenshot_path.replace('origin', 'KG_res')
            KG_path = KG_path.replace('jpg', 'png')
            picture = cv2.imread(screenshot_path, 0)
            split_dic = split(screenshot_path)
            components = self.extract_pic.generate_widget_info(screenshot_path)
            res = next_step(picture, split_dic, components, self.test_context.last_cnt_id)
            print(res)
            res = self.test_context.filter_test_node(res)
            print(res)
            bboxs = []
            for data in res['data']:
                bboxs.append(Bbox(data['x1'], data['y1'], data['x2'], data['y2']))
            pic = cv2.imread(screenshot_path)
            draw_rectangle_show_save(pic, bboxs, KG_path)
            test_node_list = [TestNode(item['category'], item['ocr'], item['operation'], item['cnt'], item['cnt_id'],
                                       item['x1'], item['y1'], item['x2'], item['y2'], item['state'],
                                       get_cur_activity_name()) for item in res['data']]
            traceback = True
            if len(test_node_list) > 0:
                cur_test_node = test_node_list[0]
                res = self.operation.get(cur_test_node.widget_operation, self.default_opera)(cur_test_node.left,
                                                                                             cur_test_node.top,
                                                                                             cur_test_node.right,
                                                                                             cur_test_node.bottom,
                                                                                             cur_test_node.cnt)
                self.test_context.add_test_node(test_node_list)
                traceback = not res
            if traceback:
                traceback_sequence = self.test_context.find_traversal_node()
                if traceback_sequence is None:
                    self.test_terminated = True
                else:
                    uninstall_appium_setting()
                    self.appium_init()
                    for test_node in traceback_sequence:
                        self.operation.get(test_node.widget_operation, self.default_opera)(test_node.left,
                                                                                           test_node.top,
                                                                                           test_node.right,
                                                                                           test_node.bottom,
                                                                                           test_node.cnt)
        return

    def appium_quit(self):
        self.driver.quit()
        self.driver = None
