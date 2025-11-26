from myutils.DeviceUtils import *
from myutils.ScreenshotUtils import *
from detect_popup import detect_pic
from detect_shadow import detect_shadow
from myutils.save_popup_context import save_popup_cur_context
from stop_and_run_uiautomator import rerun_uiautomator2
import uiautomator2 as u2

def getCurrentPackageName():
    d = u2.connect()
    info = d.info
    print(info)
    return info['currentPackageName']

def get_pop_up():
    try:
        content = get_screen_content()
        cur_activity = content["cur_activity"]
        screenshot_path = content["screenshot_path"]
        popup_widget_info = detect_pic(screenshot_path)
        LogUtils.log_info(popup_widget_info)
        if popup_widget_info is not None and len(popup_widget_info) > 0 and detect_shadow(screenshot_path,
                                                                                          popup_widget_info[0]['bounds']):
            popup = popup_widget_info[0]
            xywh = popup["bounds"]
            ltrb = get_4corner_coord_withnotpercent(xywh)
            content["ltrb"] = ltrb
            content["widget_popup"] = popup_widget_info[1:]
            # 弹框收集
            print("收集到弹框")
            save_popup_cur_context(Config.get_instance().get_collectDataPath(), screenshot_path, content["xml"],
                                   popup["bounds"], popup_widget_info[1:], cur_activity, "in-app")

        print("执行完成！")
    except u2.exceptions:
        print("弹框收集失败...")


if __name__ == '__main__':
    rerun_uiautomator2()
    curPkgName = getCurrentPackageName()
    Config.get_instance().target_pkg_name = curPkgName
    Config.get_instance().app_name = curPkgName
    get_pop_up()
