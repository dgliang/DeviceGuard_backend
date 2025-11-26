import threading, time
from queue import Queue

lock = threading.Lock()
class Consumer(threading.Thread):
    def __init__(self, t_name, queue):
        threading.Thread.__init__(self, name=t_name)
        self.data = queue

    def run(self):
        while 1:
            flag = False
            time.sleep(5)
            try:
                data = self.data.get(1, 2)
                # print()
                # print("*" * 50 + f"Consumer{self.name}" + "*" * 50)
                # print(data)
                # print("*" * 50 + f"Consumer{self.name}" + "*" * 50)
                # print()
            except:
                flag = True
            if flag == True:
                print("没有数据")
            else:
                print("有数据")

