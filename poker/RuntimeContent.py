from ScreenNode import *
from collections import deque

class ScreenShotPage:
    def __int__(self, sc_path, sc_text, ck_eles_text, cr_time):
        self.screenshot_path = sc_path
        self.screen_text = sc_text
        self.cur_ck_eles_text = ck_eles_text
        self.create_time = cr_time

class RuntimeContent(object):
    def __init__(self):
        # 存储运行时遍历过的screen序列
        self.screen_list = []
        # 存储运行时的state序列
        self.state_list = []
        # 存储因为错误导致重启的screen序列
        self.error_screen_list = []
        # 存储因为错误导致重启的clickable_ele
        self.error_clickable_ele_uid_list = []
        # 存储着整个app所有screen(ScrennNode) {key:screen_sig, val:screen_node}
        self.screen_map = {}
        # 存储着整个app所有popup(ScrennNode) {key:screen_sig, val:screen_node}
        self.popup_map = {}
        # 全局记录每个组件的uid {key:cur_clickable_ele_uid, val:clickable_ele}
        self.ele_uid_map = {}

        self.cov_mono_que = deque()
        self.screen_depth_map = {}

        # pre_screen_node在back或者click都会记录之前的界面
        self.pre_screen_node = None
        # pre_screen_shot_path表示back或者click之前的截图地址
        self.pre_screen_shot_path = None

        self.first_screen_ck_eles_text = None
        # last_screen_node和last_clickable_ele_uid只会记录click之前的, back时会重置
        self.last_clickable_ele_uid = None
        self.last_screen_node = None

        self.is_found_privacy_url = False

        self.already_click_eles = set()

        self.screenshot_uid_pair = set()

        self.similarity_mem = {}

        self.screenshot_time_list = []

    def __new__(cls, *args, **kwargs):
        if not hasattr(RuntimeContent, "_instance"):
            RuntimeContent._instance = object.__new__(cls)
        return RuntimeContent._instance

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if not hasattr(RuntimeContent, '_instance'):
            RuntimeContent._instance = RuntimeContent(*args, **kwargs)
        return RuntimeContent._instance


    def get_last_screen_node(self):
        return self.last_screen_node

    def set_last_screen_node(self, target):
        self.last_screen_node = target

    def get_last_clickable_ele_uid(self):
        return self.last_clickable_ele_uid

    def set_last_clickable_ele_uid(self, ele_uid):
        self.last_clickable_ele_uid = ele_uid

    def set_pre_screen_node(self, target):
        self.pre_screen_node = target

    def get_pre_screen_node(self):
        return self.pre_screen_node

    def set_pre_screen_shot_path(self, screenshot_path):
        self.pre_screen_shot_path = screenshot_path

    def get_pre_screen_shot_path(self):
        return self.pre_screen_shot_path

    def append_screen_list(self, ck_eles_text):
        self.screen_list.append(ck_eles_text)

    def get_screen_list(self):
        return self.screen_list

    def clear_screen_list(self):
        self.screen_list.clear()

    def append_state_list(self, state):
        self.state_list.append(state)

    def get_state_list(self):
        return self.state_list

    def clear_state_list(self):
        self.state_list.clear()

    def append_error_screen_list(self, ck_eles_text:str):
        self.error_screen_list.append(ck_eles_text)

    def get_error_screen_list(self):
        return self.error_screen_list

    def append_error_clickable_ele_uid_list(self, ele_uid:str):
        self.error_clickable_ele_uid_list.append(ele_uid)

    def append_more_error_ck_ele_uid_list(self, ele_uid_list:list):
        for ele_uid in ele_uid_list:
            self.error_clickable_ele_uid_list.append(ele_uid)

    def get_error_clickable_ele_uid_list(self):
        return self.error_clickable_ele_uid_list

    def put_screen_map(self, ck_eles_text:str, screen_node:ScreenNode):
        self.screen_map[ck_eles_text] = screen_node

    def get_screen_map(self):
        return self.screen_map

    def get_popup_map(self):
        return self.popup_map

    def put_popup_map(self, ck_eles_text:str, screen_node:ScreenNode):
        self.popup_map[ck_eles_text] = screen_node

    def put_ele_uid_map(self, ele_uid, ele_dict):
        self.ele_uid_map[ele_uid] = ele_dict

    def get_ele_uid_map_by_uid(self, uid):
        return self.ele_uid_map[uid]

    def query_simi_mem(self, key):
        if self.similarity_mem.get(key , False) == False:
            return None
        else:
            return self.similarity_mem.get(key)

    def update_simi_mem(self, key, val):
        self.similarity_mem[key] = val

    def get_similarity_mem(self):
        return self.similarity_mem

    def get_first_screen_ck_eles_text(self):
        return self.first_screen_ck_eles_text

    def set_first_screen_ck_ele_text(self, ck_eles_text):
        self.first_screen_ck_eles_text = ck_eles_text

    def add_screenshot_time_list(self, sc_path, sc_text, ck_eles_text, cr_time):
        item = {}
        item["screen_shot_path"] = sc_path
        item["screen_text"] = sc_text
        item["ck_eles_text"] = ck_eles_text
        item["create_time"] = cr_time
        self.screenshot_time_list.append(item)

    def get_screenshot_time_list(self):
        return self.screenshot_time_list