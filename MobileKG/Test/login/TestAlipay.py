import cv2
import json
from MobileKG.LayoutAnalysis.LayoutMain import split
from MobileKG.SearchKG.SearchMain import next_step


def test_pic_1():
    picture = cv2.imread('alipay_login/screenshots/alipay1.jpg', 0)
    split_dic = split('alipay_login/screenshots/alipay1.jpg')
    components = {
        "components": json.loads(open('alipay_login/analyzed_json/alipay1.json', 'r', encoding='utf-8').read())
    }
    print('Result for Pic 1:')
    # {'status': 'success', 'data': [{'category': 'ImageView', 'ocr': '同意', 'operation': '点击', 'cnt': '同意', 'cnt_id': 1, 'x1': 695, 'y1': 1872, 'x2': 805, 'y2': 1926}]}
    print(next_step(picture, split_dic, components, 0, False))
    return


def test_pic_2():
    picture = cv2.imread('alipay_login/screenshots/alipay2.jpg', 0)
    split_dic = split('alipay_login/screenshots/alipay2.jpg')
    components = {
        "components": json.loads(open('alipay_login/analyzed_json/alipay2.json', 'r', encoding='utf-8').read())
    }
    print('Result for Pic 2:')
    # {'status': 'success', 'data': [{'category': 'TextView', 'ocr': '淘淘宝登录', 'operation': '点击', 'cnt': '淘宝登录', 'cnt_id': 68, 'x1': 421, 'y1': 2114, 'x2': 674, 'y2': 2173}, {'category': 'TextView', 'ocr': '邮箱登录', 'operation': '点击', 'cnt': '邮箱登录', 'cnt_id': 35, 'x1': 829, 'y1': 2114, 'x2': 1024, 'y2': 2173}, {'category': 'TextView', 'ocr': '输入手机号,使用支付宝', 'operation': '点击', 'cnt': '输入手机号，使用支付宝', 'cnt_id': 2, 'x1': 265, 'y1': 1555, 'x2': 792, 'y2': 1610}]}
    print(next_step(picture, split_dic, components, 1, False))
    return


def test_pic_3():
    picture = cv2.imread('alipay_login/screenshots/alipay3.jpg', 0)
    split_dic = split('alipay_login/screenshots/alipay3.jpg')
    components = {
        "components": json.loads(open('alipay_login/analyzed_json/alipay3.json', 'r', encoding='utf-8').read())
    }
    print('Result for Pic 3:')
    # {'status': 'success', 'data': [{'category': 'TextView', 'ocr': '输入手机号登录', 'operation': '输入', 'cnt': '手机号', 'cnt_id': 3, 'x1': 243, 'y1': 347, 'x2': 859, 'y2': 454}]}
    print(next_step(picture, split_dic, components, 2, False))
    return


def test_pic_4():
    picture = cv2.imread('alipay_login/screenshots/alipay4.jpg', 0)
    split_dic = split('alipay_login/screenshots/alipay4.jpg')
    components = {
        "components": json.loads(open('alipay_login/analyzed_json/alipay4.json', 'r', encoding='utf-8').read())
    }
    print('Result for Pic 4:')
    # {'status': 'success', 'data': [{'category': 'TextView', 'ocr': '下一步', 'operation': '点击', 'cnt': '下一步', 'cnt_id': 4, 'x1': 462, 'y1': 828, 'x2': 628, 'y2': 891}]}
    print(next_step(picture, split_dic, components, 3, False))
    return


def test_pic_5():
    picture = cv2.imread('alipay_login/screenshots/alipay5.jpg', 0)
    split_dic = split('alipay_login/screenshots/alipay5.jpg')
    components = {
        "components": json.loads(open('alipay_login/analyzed_json/alipay5.json', 'r', encoding='utf-8').read())
    }
    print('Result for Pic 5:')
    # {'status': 'success', 'data': [{'category': 'TextView', 'ocr': '不同意', 'operation': '点击', 'cnt': '同意', 'cnt_id': 1, 'x1': 252, 'y1': 1290, 'x2': 401, 'y2': 1350}]}
    print(next_step(picture, split_dic, components, 4, False))
    return


def test_pic_6():
    picture = cv2.imread('alipay_login/screenshots/alipay6.jpg', 0)
    split_dic = split('alipay_login/screenshots/alipay6.jpg')
    components = {
        "components": json.loads(open('alipay_login/analyzed_json/alipay6.json', 'r', encoding='utf-8').read())
    }
    print('Result for Pic 6:')
    # {'status': 'success', 'data': [{'category': 'TextView', 'ocr': '换个方式登录', 'operation': '点击', 'cnt': '换个方式登录', 'cnt_id': 13, 'x1': 395, 'y1': 1297, 'x2': 687, 'y2': 1355}, {'category': 'TextView', 'ocr': '刷脸登录', 'operation': '点击', 'cnt': '刷脸登录', 'cnt_id': 6, 'x1': 441, 'y1': 1145, 'x2': 650, 'y2': 1204}]}
    print(next_step(picture, split_dic, components, 1, False))
    return


def test_pic_7():
    picture = cv2.imread('alipay_login/screenshots/alipay7.jpg', 0)
    split_dic = split('alipay_login/screenshots/alipay7.jpg')
    components = {
        "components": json.loads(open('alipay_login/analyzed_json/alipay7.json', 'r', encoding='utf-8').read())
    }
    print('Result for Pic 7:')
    # {'status': 'success', 'data': [{'category': 'ImageView', 'ocr': '关闭', 'operation': '点击', 'cnt': '关闭', 'cnt_id': 7, 'x1': 956, 'y1': 126, 'x2': 1046, 'y2': 180}]}
    print(next_step(picture, split_dic, components, 6, False))
    # {'status': 'success', 'data': [{'category': 'ImageView', 'ocr': '关闭', 'operation': '点击', 'cnt': '关闭', 'cnt_id': 7, 'x1': 956, 'y1': 126, 'x2': 1046, 'y2': 180}]}
    print(next_step(picture, split_dic, components, 24, False))
    return


def test_pic_8():
    picture = cv2.imread('alipay_login/screenshots/alipay8.jpg', 0)
    split_dic = split('alipay_login/screenshots/alipay8.jpg')
    components = {
        "components": json.loads(open('alipay_login/analyzed_json/alipay8.json', 'r', encoding='utf-8').read())
    }
    print('Result for Pic 8:')
    # {'status': 'success', 'data': [{'category': 'ImageView', 'ocr': '同意', 'operation': '点击', 'cnt': '同意', 'cnt_id': 1, 'x1': 697, 'y1': 1290, 'x2': 814, 'y2': 1350}]}
    print(next_step(picture, split_dic, components, 68, False))
    return


def test_pic_9():
    picture = cv2.imread('alipay_login/screenshots/alipay9.jpg', 0)
    split_dic = split('alipay_login/screenshots/alipay9.jpg')
    components = {
        "components": json.loads(open('alipay_login/analyzed_json/alipay9.json', 'r', encoding='utf-8').read())
    }
    print('Result for Pic 9:')
    # {'status': 'success', 'data': [{'category': 'TextView', 'ocr': '确认授权', 'operation': '点击', 'cnt': '确认授权', 'cnt_id': 33, 'x1': 454, 'y1': 1266, 'x2': 635, 'y2': 1317}]}
    print(next_step(picture, split_dic, components, 1, False))
    # {'status': 'success', 'data': [{'category': 'TextView', 'ocr': '确认授权', 'operation': '点击', 'cnt': '确认授权', 'cnt_id': 33, 'x1': 454, 'y1': 1266, 'x2': 635, 'y2': 1317}]}
    print(next_step(picture, split_dic, components, 32, False))
    return


def test_pic_10():
    picture = cv2.imread('alipay_login/screenshots/alipay10.jpg', 0)
    split_dic = split('alipay_login/screenshots/alipay10.jpg')
    components = {
        "components": json.loads(open('alipay_login/analyzed_json/alipay10.json', 'r', encoding='utf-8').read())
    }
    print('Result for Pic 10:')
    # {'status': 'success', 'data': [{'category': 'TextView', 'ocr': '请输入手机号/邮箱/淘宝会员名', 'operation': '输入', 'cnt': '手机号邮箱淘宝会员名', 'cnt_id': 36, 'x1': 66, 'y1': 941, 'x2': 759, 'y2': 1003}]}
    print(next_step(picture, split_dic, components, 35, False))
    return


def test_pic_11():
    picture = cv2.imread('alipay_login/screenshots/alipay11.jpg', 0)
    split_dic = split('alipay_login/screenshots/alipay11.jpg')
    components = {
        "components": json.loads(open('alipay_login/analyzed_json/alipay11.json', 'r', encoding='utf-8').read())
    }
    print('Result for Pic 11:')
    # {'status': 'success', 'data': [{'category': 'ImageView', 'ocr': '同意', 'operation': '点击', 'cnt': '同意', 'cnt_id': 1, 'x1': 697, 'y1': 1290, 'x2': 815, 'y2': 1349}]}
    print(next_step(picture, split_dic, components, 4, False))
    return


def test_pic_12():
    picture = cv2.imread('alipay_login/screenshots/alipay12.jpg', 0)
    split_dic = split('alipay_login/screenshots/alipay12.jpg')
    components = {
        "components": json.loads(open('alipay_login/analyzed_json/alipay12.json', 'r', encoding='utf-8').read())
    }
    print('Result for Pic 12:')
    # {'status': 'success', 'data': [{'category': 'TextView', 'ocr': '淘宝用户快速登录', 'operation': '点击', 'cnt': '淘宝用户快速登录', 'cnt_id': 32, 'x1': 199, 'y1': 1207, 'x2': 581, 'y2': 1262}, {'category': 'TextView', 'ocr': '密码登录', 'operation': '点击', 'cnt': '密码登录', 'cnt_id': 22, 'x1': 201, 'y1': 1063, 'x2': 385, 'y2': 1115}, {'category': 'TextView', 'ocr': '短信验证码登录', 'operation': '点击', 'cnt': '短信验证码登录', 'cnt_id': 14, 'x1': 198, 'y1': 916, 'x2': 531, 'y2': 973}]}
    print(next_step(picture, split_dic, components, 13, False))
    return


def test_pic_13():
    picture = cv2.imread('alipay_login/screenshots/alipay13.jpg', 0)
    split_dic = split('alipay_login/screenshots/alipay13.jpg')
    components = {
        "components": json.loads(open('alipay_login/analyzed_json/alipay13.json', 'r', encoding='utf-8').read())
    }
    print('Result for Pic 13:')
    # {'status': 'success', 'data': [{'category': 'TextView', 'ocr': '短信验证码登录', 'operation': '点击', 'cnt': '短信验证码登录', 'cnt_id': 14, 'x1': 362, 'y1': 1142, 'x2': 729, 'y2': 1204}]}
    print(next_step(picture, split_dic, components, 14, False))
    return


def test_pic_14():
    picture = cv2.imread('alipay_login/screenshots/alipay14.jpg', 0)
    split_dic = split('alipay_login/screenshots/alipay14.jpg')
    components = {
        "components": json.loads(open('alipay_login/analyzed_json/alipay14.json', 'r', encoding='utf-8').read())
    }
    print('Result for Pic 14:')
    # {'status': 'success', 'data': [{'category': 'TextView', 'ocr': '请输入登录密码', 'operation': '输入', 'cnt': '密码', 'cnt_id': 23, 'x1': 57, 'y1': 1046, 'x2': 429, 'y2': 1107}]}
    print(next_step(picture, split_dic, components, 22, False))
    return


def test_pic_15():
    picture = cv2.imread('alipay_login/screenshots/alipay15.jpg', 0)
    split_dic = split('alipay_login/screenshots/alipay15.jpg')
    components = {
        "components": json.loads(open('alipay_login/analyzed_json/alipay15.json', 'r', encoding='utf-8').read())
    }
    print('Result for Pic 15:')
    # {'status': 'success', 'data': [{'category': 'TextView', 'ocr': '下一步', 'operation': '点击', 'cnt': '下一步', 'cnt_id': 4, 'x1': 470, 'y1': 1203, 'x2': 617, 'y2': 1263}]}
    print(next_step(picture, split_dic, components, 36, False))
    return


def test_pic_16():
    picture = cv2.imread('alipay_login/screenshots/alipay16.jpg', 0)
    split_dic = split('alipay_login/screenshots/alipay16.jpg')
    components = {
        "components": json.loads(open('alipay_login/analyzed_json/alipay16.json', 'r', encoding='utf-8').read())
    }
    print('Result for Pic 16:')
    # {'status': 'success', 'data': [{'category': 'ImageView', 'ocr': '登录', 'operation': '点击', 'cnt': '登录', 'cnt_id': 24, 'x1': 493, 'y1': 1249, 'x2': 595, 'y2': 1308}]}
    print(next_step(picture, split_dic, components, 23, False))
    return

def test_new_pic_1():
    picture = cv2.imread('new_alipay_login/screenshots/1.png', 0)
    split_dic = split('new_alipay_login/screenshots/1.png')
    components = {
        "components": json.loads(open('new_alipay_login/analyzed_json/1.json', 'r', encoding='utf-8').read())
    }
    print('Result for New Pic 1:')
    # {'status': 'success', 'data': [{'category': 'ImageView', 'ocr': '登录', 'operation': '点击', 'cnt': '登录', 'cnt_id': 24, 'x1': 493, 'y1': 1249, 'x2': 595, 'y2': 1308}]}
    print(next_step(picture, split_dic, components, 1, False))
    return

def test_new_pic_2():
    picture = cv2.imread('new_alipay_login/screenshots/2.png', 0)
    split_dic = split('new_alipay_login/screenshots/2.png')
    components = {
        "components": json.loads(open('new_alipay_login/analyzed_json/2.json', 'r', encoding='utf-8').read())
    }
    print('Result for New Pic 2:')
    # {'status': 'success', 'data': [{'category': 'ImageView', 'ocr': '登录', 'operation': '点击', 'cnt': '登录', 'cnt_id': 24, 'x1': 493, 'y1': 1249, 'x2': 595, 'y2': 1308}]}
    print(next_step(picture, split_dic, components, 2, False))
    return
# test_pic_2()
# test_pic_3()
# test_pic_8()
# test_pic_10()
#
# test_pic_4() # {'status': 'success', 'data': [{'category': 'ImageView', 'ocr': '+86', 'operation': '输入', 'cnt': '密码', 'cnt_id': 23, 'x1': 96, 'y1': 628, 'x2': 177, 'y2': 674}, {'category': 'TextView', 'ocr': '下一步', 'operation': '点击', 'cnt': '下一步', 'cnt_id': 4, 'x1': 462, 'y1': 828, 'x2': 628, 'y2': 891}, {'category': 'Button', 'ocr': '', 'operation': '输入', 'cnt': '手机号', 'cnt_id': 3, 'x1': 55, 'y1': 572, 'x2': 1025, 'y2': 729}]}
# test_pic_15()
# test_pic_9()
#
# test_pic_5()
# test_pic_11()
#
# test_pic_6()
# test_pic_7()
# test_pic_12() # {'status': 'success', 'data': [{'category': 'TextView', 'ocr': '淘宝用户快速登录', 'operation': '点击', 'cnt': '淘宝用户快速登录', 'cnt_id': 32, 'x1': 199, 'y1': 1207, 'x2': 581, 'y2': 1262}, {'category': 'TextView', 'ocr': '密码登录', 'operation': '点击', 'cnt': '密码登录', 'cnt_id': 22, 'x1': 201, 'y1': 1063, 'x2': 385, 'y2': 1115}, {'category': 'TextView', 'ocr': '短信验证码登录', 'operation': '点击', 'cnt': '短信验证码登录', 'cnt_id': 14, 'x1': 198, 'y1': 916, 'x2': 531, 'y2': 973}, {'category': 'TextView', 'ocr': '更多登录方式', 'operation': '点击', 'cnt': '更登录方式', 'cnt_id': 94, 'x1': 202, 'y1': 1354, 'x2': 472, 'y2': 1407}]}
# test_pic_13()
# test_pic_14() # {'status': 'success', 'data': [{'category': 'ImageView', 'ocr': '登录', 'operation': '点击', 'cnt': '登录', 'cnt_id': 24, 'x1': 492, 'y1': 1250, 'x2': 593, 'y2': 1309}, {'category': 'TextView', 'ocr': '请输入登录密码', 'operation': '输入', 'cnt': '密码', 'cnt_id': 23, 'x1': 57, 'y1': 1046, 'x2': 429, 'y2': 1107}]}
# test_pic_16()

test_new_pic_2()