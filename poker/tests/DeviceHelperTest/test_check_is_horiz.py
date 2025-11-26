from utils.DeviceUtils import check_is_horiz
from utils.DeviceUtils import get_xml
root= get_xml()
print(root)
res = check_is_horiz(root)
print(res)