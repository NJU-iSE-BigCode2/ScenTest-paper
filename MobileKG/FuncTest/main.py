import MobileKG.FuncTest.test_app as test_app
import MobileKG.FuncTest.run_command as run_command

if __name__ == '__main__':
    package, activity, path = run_command.get_app_info('jlb.apk')
    atuo_test_tool = test_app.AutoTestTool(package, activity, path)
    atuo_test_tool.appium_init()
    atuo_test_tool.test_by_KG()
