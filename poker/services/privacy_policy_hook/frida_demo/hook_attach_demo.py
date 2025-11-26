import sys
import frida


def on_message(message, data):
    print(message)


device = frida.get_usb_device()
# 启动`demo02`这个app
print(device)
pid = device.attach("fridademo")
# 加载s1.js脚本
with open("hook.js") as f:
    script = pid.create_script(f.read())
script.on('message', on_message)
script.load()
sys.stdin.read()
