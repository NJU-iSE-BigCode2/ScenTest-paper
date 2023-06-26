import cv2
import json
from MobileKG.LayoutAnalysis.LayoutMain import split
from MobileKG.SearchKG.SearchMain import next_step
from MobileKG.GenerateKG.operation.MessageCompare import MessageCompare


def test_pic(num, last_cnt_id):
    picture = cv2.imread('login/other_login/test' + num + '.png', 0)
    split_dic = split('login/other_login/test' + num + '.png')
    components = {
        "components": json.loads(open('login/other_login/test' + num + '.json', 'r', encoding='utf-8').read())
    }
    print('Result for Pic 5:')
    print(next_step(picture, split_dic, components, last_cnt_id, False))
    return


# test_pic('01', 0)
# test_pic('02', 1)
# test_pic('03', 1)
# test_pic('04', 72)
# test_pic('05', 24)
# test_pic('06',202)
# test_pic('07',164)
# test_pic('09',111)
# test_pic('10',75)
# test_pic('11',22)
# test_pic('12',72)
# test_pic('13',76)
# test_pic('14',0)
# test_pic('15',1)
# test_pic('17',71)
# test_pic('18',22)
# test_pic('19',340)
# test_pic('21',111)
# test_pic('24',332)
test_pic('25',1)
# print(MessageCompare.txt_sim('手机号','输入手机号用于绑定'))