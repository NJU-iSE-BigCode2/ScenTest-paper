import cv2
import json
from MobileKG.LayoutAnalysis.LayoutMain import split
from MobileKG.SearchKG.SearchMain import next_step


def test_pic_1():
    picture = cv2.imread('58city_login/58city01.png', 0)
    split_dic = split('58city_login/58city01.png')
    components = {
        "components": json.loads(open('58city_login/58city01.json', 'r', encoding='utf-8').read())
    }
    print('Result for Pic 1:')
    print(next_step(picture, split_dic, components, 0, False))
    return

def test_pic_2():
    picture = cv2.imread('58city_login/58city02.png', 0)
    split_dic = split('58city_login/58city02.png')
    components = {
        "components": json.loads(open('58city_login/58city02.json', 'r', encoding='utf-8').read())
    }
    print('Result for Pic 2:')
    print(next_step(picture, split_dic, components, 24, False))
    return

def test_pic_3():
    picture = cv2.imread('58city_login/58city03.png', 0)
    split_dic = split('58city_login/58city03.png')
    components = {
        "components": json.loads(open('58city_login/58city03.json', 'r', encoding='utf-8').read())
    }
    print('Result for Pic 3:')
    print(next_step(picture, split_dic, components, 137, False))
    return

test_pic_3()
