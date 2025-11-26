
from StateHandler import *
from myutils.CalDepthUtils import *
from hashlib import md5
from myutils.PrivacyUrlUtils import *

hash_md5 = md5()


def get_random_str():
    str = ''.join(random.sample(
        ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e',
         'd', 'c', 'b', 'a'], 10))
    return str
# def copy_image_as_byte_stream(from_img_source_path, from_img_save_path, to_img_source_path, to_img_save_path):
#     # Copy from_img_full_path to from_img_path
#     with open(from_img_source_path, 'rb') as f:
#         byte_stream = f.read()
#         with open(from_img_save_path, 'wb') as f_out:
#             f_out.write(byte_stream)
#
#     # Copy to_img_full_path to to_img_path
#     with open(to_img_source_path, 'rb') as f:
#         byte_stream = f.read()
#         with open(to_img_save_path, 'wb') as f_out:
#             f_out.write(byte_stream)

def copy_image_as_byte_stream(source, target):
    # Copy from_img_full_path to from_img_path
    with open(source, 'rb') as f:
        byte_stream = f.read()
        with open(target, 'wb') as f_out:
            f_out.write(byte_stream)

def save_popup_postcontext(screenshot_path, screen_text, ck_eles_text):
    pre_scshot_path = RuntimeContent.get_instance().get_pre_screen_shot_path()
    pre_screen_node = RuntimeContent.get_instance().get_pre_screen_node()
    popup_map = RuntimeContent.get_instance().get_popup_map()
    # 前一个界面非弹框则return
    if pre_screen_node not in popup_map.values():
        return
    pre_text = ""
    pre_ck_eles_text = ""
    if pre_screen_node is not None:
        pre_text = pre_screen_node.screen_text
        pre_ck_eles_text = pre_screen_node.ck_eles_text

    last_clickable_ele_uid = RuntimeContent.get_instance().get_last_clickable_ele_uid()
    click_text = "dummy_root_element"
    click_xy = (-1, -1)
    if last_clickable_ele_uid != "dummy_root_element" and last_clickable_ele_uid != "":
        click_xy = get_location(
            RuntimeContent.get_instance().get_ele_uid_map_by_uid(last_clickable_ele_uid))
        click_text = RuntimeContent.get_instance().get_ele_uid_map_by_uid(last_clickable_ele_uid)["text"]

    suid_pair = (pre_text, click_text)
    if suid_pair not in RuntimeContent.get_instance().screenshot_uid_pair:
        save_popup_postcontextsub(Config.get_instance().get_collectDataPath(), pre_scshot_path, screenshot_path,
                           click_xy,
                           click_text, pre_text, screen_text, pre_ck_eles_text, ck_eles_text, "PopupPostContext", pre_screen_node.ck_eles_text)
        RuntimeContent.get_instance().screenshot_uid_pair.add(suid_pair)

def save_popup_precontext(screenshot_path, screen_text, ck_eles_text):
    pre_scshot_path = RuntimeContent.get_instance().get_pre_screen_shot_path()
    pre_screen_node = RuntimeContent.get_instance().get_pre_screen_node()
    pre_text = ""
    pre_ck_eles_text = ""
    if pre_screen_node is not None:
        pre_text = pre_screen_node.screen_text
        pre_ck_eles_text = pre_screen_node.ck_eles_text

    last_clickable_ele_uid = RuntimeContent.get_instance().get_last_clickable_ele_uid()
    click_text = "dummy_root_element"
    click_xy = (-1, -1)
    if last_clickable_ele_uid != "dummy_root_element" and last_clickable_ele_uid != "":
        click_xy = get_location(
            RuntimeContent.get_instance().get_ele_uid_map_by_uid(last_clickable_ele_uid))
        click_text = RuntimeContent.get_instance().get_ele_uid_map_by_uid(last_clickable_ele_uid)["text"]

    suid_pair = (pre_text, click_text)
    if suid_pair not in RuntimeContent.get_instance().screenshot_uid_pair:
        save_popup_context(Config.get_instance().get_collectDataPath(), pre_scshot_path, screenshot_path,
                           click_xy,
                           click_text, pre_text, screen_text, pre_ck_eles_text, ck_eles_text, "PopupPreContext")
        RuntimeContent.get_instance().screenshot_uid_pair.add(suid_pair)


def save_popup_postcontextsub(abs_path: str, from_img: str, to_img: str, click_xy: tuple, click_text:str, from_text:str, to_text:str, pre_ck_eles_text:str, ck_eles_text:str, name:str, uid:str):
    # 创建文件夹名,获取包名
    # package_name = abs_path.split("\\")[-1].split("-")[0]

    h_md5 = hash_md5.copy()
    h_md5.update(uid.encode('utf-8'))
    md5_str = h_md5.hexdigest()

    # 加上时间戳
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    time_path = f"{timestamp}"
    abs_dir = os.getcwd()
    #获取当前文件所在目录
    base_directory = abs_path
    screenshot_dir = os.path.join(abs_dir, base_directory, "Screenshot", "ScreenshotPicture")

    from_img = os.path.split(from_img)[-1]
    to_img = os.path.split(to_img)[-1]

    # 保存图片
    from_img_path = os.path.join(screenshot_dir, f"{from_img}")
    to_img_path = os.path.join(screenshot_dir, f"{to_img}")

    popup_dir = os.path.join(abs_dir, base_directory, name, md5_str, time_path)
    os.makedirs(popup_dir)
    from_img_save_path = os.path.join(popup_dir, from_img)
    to_img_save_path = os.path.join(popup_dir, to_img)

    if "root" not in from_img_path:
        copy_image_as_byte_stream(from_img_path, from_img_save_path)
    if "root" not in to_img_path:
        copy_image_as_byte_stream(to_img_path, to_img_save_path)

    json_full_path = os.path.join(popup_dir, "ui_relations.json")

    # 保存到json文件

    res_dict = {}
    res_dict["from_img"] = from_img
    res_dict["to_img"] = to_img
    res_dict["click_text"] = click_text
    res_dict["click_xy"] = click_xy
    res_dict["from_text"] = from_text
    res_dict["to_text"] = to_text
    res_dict["from_ck_eles_text"] = pre_ck_eles_text
    res_dict["to_ck_eles_text"] = ck_eles_text
    with open(json_full_path, "w", encoding='utf-8') as file:
        json.dump(res_dict, file, ensure_ascii=False)


def save_popup_context(abs_path: str, from_img: str, to_img: str, click_xy: tuple, click_text:str, from_text:str, to_text:str, pre_ck_eles_text:str, ck_eles_text:str, name:str):
    # 创建文件夹名,获取包名
    # package_name = abs_path.split("\\")[-1].split("-")[0]

    # 加上时间戳
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    time_path = f"{timestamp}"
    abs_dir = os.getcwd()
    #获取当前文件所在目录
    base_directory = abs_path
    screenshot_dir = os.path.join(abs_dir, base_directory, "Screenshot", "ScreenshotPicture")

    from_img = os.path.split(from_img)[-1]
    to_img = os.path.split(to_img)[-1]

    # 保存图片
    from_img_path = os.path.join(screenshot_dir, f"{from_img}")
    to_img_path = os.path.join(screenshot_dir, f"{to_img}")

    popup_dir = os.path.join(abs_dir, base_directory, name, time_path)
    os.makedirs(popup_dir)
    from_img_save_path = os.path.join(popup_dir, from_img)
    to_img_save_path = os.path.join(popup_dir, to_img)

    if "root" not in from_img_path:
        copy_image_as_byte_stream(from_img_path, from_img_save_path)
    if "root" not in to_img_path:
        copy_image_as_byte_stream(to_img_path, to_img_save_path)

    json_full_path = os.path.join(popup_dir, "ui_relations.json")

    # 保存到json文件

    res_dict = {}
    res_dict["from_img"] = from_img
    res_dict["to_img"] = to_img
    res_dict["click_text"] = click_text
    res_dict["click_xy"] = click_xy
    res_dict["from_text"] = from_text
    res_dict["to_text"] = to_text
    res_dict["from_ck_eles_text"] = pre_ck_eles_text
    res_dict["to_ck_eles_text"] = ck_eles_text
    with open(json_full_path, "w", encoding='utf-8') as file:
        json.dump(res_dict, file, ensure_ascii=False)


def save_popup_img(abs_path: str, to_img: str):
    # 创建文件夹名,获取包名
    # package_name = abs_path.split("\\")[-1].split("-")[0]
    abs_dir = os.getcwd()
    #获取当前文件所在目录
    base_directory = abs_path
    screenshot_dir = os.path.join(abs_dir, base_directory, "Screenshot", "ScreenshotPicture")

    to_img = os.path.split(to_img)[-1]

    # 保存图片
    to_img_path = os.path.join(screenshot_dir, f"{to_img}")
    popup_dir = os.path.join(abs_dir, base_directory, "PopupImg")
    if not os.path.exists(popup_dir):
        os.makedirs(popup_dir)

    to_img_save_path = os.path.join(popup_dir, to_img)

    if "root" not in to_img_path:
        copy_image_as_byte_stream(to_img_path, to_img_save_path)


def save_popup_cur_context(abs_path: str, to_img: str, xml_str:str, pow_bounds, pow_ele, activity_name, type_name):
    # 创建文件夹名,获取包名
    # package_name = abs_path.split("\\")[-1].split("-")[0]
    abs_dir = os.getcwd()
    #获取当前文件所在目录
    base_directory = abs_path
    screenshot_dir = os.path.join(abs_dir, base_directory, "Screenshot", "ScreenshotPicture")

    to_img = os.path.split(to_img)[-1]

    # 保存图片
    to_img_path = os.path.join(screenshot_dir, f"{to_img}")
    popup_dir = os.path.join(abs_dir, base_directory, "PopupImg")
    if not os.path.exists(popup_dir):
        os.makedirs(popup_dir)

    to_img_save_path = os.path.join(popup_dir, to_img)

    if "root" not in to_img_path:
        copy_image_as_byte_stream(to_img_path, to_img_save_path)

    xml_filepath = os.path.join(popup_dir, to_img + '.xml')
    with open(xml_filepath, 'w', encoding='utf-8') as xml_file:
        xml_file.write(xml_str)


    pow = {
        "type": type_name,
        "pkg_name": Config.get_instance().target_pkg_name,
        "app_name": Config.get_instance().app_name,
        "activity_name": activity_name,
        "pow_bounds":pow_bounds,
        "pow_ele":pow_ele,
        "img_name":to_img,
    }
    json_str = json.dumps(pow, indent=4, ensure_ascii=False)
    json_filepath = os.path.join(popup_dir, to_img + '.json')
    # 将 JSON 字符串写入文件
    with open(json_filepath, "w", encoding="utf-8") as f:
        f.write(json_str)





