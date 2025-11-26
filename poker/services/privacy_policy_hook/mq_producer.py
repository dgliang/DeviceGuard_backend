import queue
import threading, time
from queue import Queue
from myutils.LogUtils import *
import frida
import re
from Config import *
from urllib.parse import unquote

lock = threading.Lock()

class FridaHookService(threading.Thread):
    def __init__(self, t_name: str, queue: Queue, daemon: bool):
        threading.Thread.__init__(self, name=t_name, daemon=daemon)
        self.data = queue
        self._stop_event = threading.Event()

    def is_http(self, test_str):
        # 使用re模块进行匹配

        pattern = r'http[s]?://(?:[a-zA-Z0-9_=.:\/?&#\-@+\*]|(?:%5F|%3D|%2E|%3A|%2F|%3F|%26|%23|%2D|%40|%2B|%2A|%3B))+|http[s]?%3A%2F%2F(?:[a-zA-Z0-9_=.:\/?&#$\-@+]|(?:%5F|%3D|%2E|%3A|%2F|%3F|%26|%23|%2D|%40|%2B|%2A|%3B))+'
        matches = re.findall(pattern, test_str)
        if not matches:
            return None

        # 去掉re返回的多余分组和作为正则表达式的url
        url_list = []
        for url in matches:
            if url.startswith('http') and not url.endswith('.') and not url.endswith('.*'):
                url_list.append(url)

        # 对url编码进行解码
        decoded_urls = [unquote(url).rstrip('\\') for url in url_list]

        # 返回url列表
        return decoded_urls

    def on_message(self, message, data):
        with lock:

            if message.get('type') != 'send':
                return
            payload = message.get('payload')
            if payload is None:
                return
            res = self.is_http(payload)
            if res:
                # print()
                # print("*" * 50 + f"Producer{self.name}" + "*" * 50)
                # print(res)
                # print("*" * 50 + f"Producer{self.name}" + "*" * 50)
                # print()
                self.data.put(res)
            # print("%s: %s is producing %d to the queue!" % (time.ctime(), self.name, message))

    def run(self):
        device = frida.get_usb_device()
        # 连接模拟器
        # device = frida.get_remote_device()

        # 启动`demo02`这个app
        appName = Config.get_instance().app_name
        pid = device.attach(appName)
        # 加载s1.js脚本

        # with open("./hook_rpc.js",encoding="utf-8") as f:
        with open("./services/privacy_policy_hook/hook_rpc.js") as f:
            script = pid.create_script(f.read())
        script.on('message', self.on_message)
        script.load()
        sys.stdin.read()
        # while not self._stop_event.is_set():
        #     pass


    def stop(self):
        self._stop_event.set()



def restart_thread(thread):
    queue = Queue()
    thread.stop()
    new_thread = FridaHookService('FridaHookService', queue, daemon=True)
    new_thread.start()
