import os
import subprocess
import time

project_dir = os.path.dirname(os.path.abspath(__file__))


def get_app_info(apk_name):
    apk_path = os.path.join(project_dir, 'apk', apk_name, '.apk')
    if not os.path.exists(apk_path):
        print("Apk file not exist!")
        return
    command = 'aapt dump badging {}'.format(apk_path)
    popen = subprocess.Popen(command,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             universal_newlines=True,
                             bufsize=1,
                             encoding='utf-8')
    out, err = popen.communicate()
    package_name = ''
    launchable_activity = ''
    items = out.split("\n") 
    item_list = [x for x in items if x != '']
    print(item_list)
    for item in item_list:
        tmp = item.split(': ')
        if len(tmp) < 2:
            continue
        item_prefix = tmp[0]
        item_vals = tmp[1]
        if item_prefix == 'package':
            val_list = item_vals.split(' ')
            for val in val_list:
                if val.split('=')[0] == 'name':
                    package_name = val.split('=')[1]
                    package_name = package_name[1:len(package_name) - 1]
                    break
        elif item_prefix == 'launchable-activity':
            val_list = item_vals.split(' ')
            for val in val_list:
                if val.split('=')[0] == 'name':
                    launchable_activity = val.split('=')[1]
                    launchable_activity = launchable_activity[1:len(launchable_activity) - 1]
                    break
    return package_name, launchable_activity, apk_path


def check_device_connected():
    with os.popen(r'adb devices', 'r') as f:
        text = f.read()
    print(text)
    s = text.split("\n")
    result = [x for x in s if x != '']
    print(result)
    devices = []
    for i in result:
        dev = i.split("\tdevice")
        if len(dev) >= 2:
            devices.append(dev[0])
    if not devices:
        return False
    else:
        return True


def get_cur_activity_name():
    with os.popen(r'adb shell dumpsys window | findstr mCurrentFocus', 'r') as f:
        text = f.read()
    activity_name = text.split("/")[-1][:-2]
    return activity_name


def get_screenshot(func_name, apk_name):
    cur_activity = get_cur_activity_name().split(".")[-1]
    pic_dir = os.path.join(project_dir, 'screenshot', func_name, apk_name, 'origin')
    imgs_name = []
    for root, dirs, files in os.walk(pic_dir):
        imgs_name = [(file.split(".")[0]).split("_")[0] for file in files]
    times = imgs_name.count(cur_activity)
    pic_name = '{}_{}.png'.format(cur_activity, times + 1)
    screenshot_command = 'adb shell screencap -p /sdcard/01.png'
    os.system(screenshot_command)
    time.sleep(2)
    screenshot_path = os.path.join(project_dir, 'screenshot', func_name, apk_name, 'origin', pic_name)
    pull_command = 'adb pull /sdcard/01.png {}'.format(screenshot_path)
    os.system(pull_command)
    time.sleep(2)
    return screenshot_path


def get_xml(apk_name):
    cur_activity = get_cur_activity_name().split(".")[-1]
    xml_command = 'adb shell uiautomator dump /sdcard/cur.xml'
    os.system(xml_command)
    time.sleep(2)
    xml_path = os.path.join(project_dir, 'xml', apk_name, '{}.xml'.format(cur_activity))
    pull_command = 'adb pull /sdcard/cur.xml {}'.format(xml_path)
    os.system(pull_command)
    time.sleep(2)
    return xml_path


def input_text(content):
    cmd_command = "adb shell input text {}".format(content)
    os.system(cmd_command)
    time.sleep(2)


def uninstall_app(app_package_name):
    uninstall_command = 'adb uninstall {}'.format(app_package_name)
    os.system(uninstall_command)
    time.sleep(2)


def uninstall_appium_setting():
    uninstall_command = 'adb uninstall io.appium.settings'
    os.system(uninstall_command)
    time.sleep(2)
    uninstall_command = 'adb uninstall io.appium.unlock'
    os.system(uninstall_command)
    time.sleep(2)


if __name__ == '__main__':
    print(get_screenshot("login", "58city"))
