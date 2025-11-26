import sys
import frida


def on_message(message, data):
    print(message)


device = frida.get_usb_device(timeout=1)
pid = device.spawn(["com.eg.android.AlipayGphone"])
session = device.attach(pid)
# 加载s1.js脚本
with open("hook_rpc.js") as f:
    script = session.create_script(f.read())
script.on('message', on_message)
script.load()
frida.resume(pid)
sys.stdin.read()
