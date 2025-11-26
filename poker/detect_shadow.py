import os

import cv2
import numpy as np
def test_single(path):
    """
    测试用，不需要传入弹框区域，只返回阴影面积的比例
    """
    # src = cv2.imread(r"D:\PythonCode\monkey\deduplicate_result_0402\monkey\com.baidu.haokan\qblpwfcuezdvgnxjsroh_deduplicate\popup_killed\1024inohx.png")
    # src = cv2.imread(r"C:\Users\17180\AppUIAutomator2Navigation\data_819\Images\empty\1VlYIadxaqULVmvb3EjNiVji8u87o6BKWcg5jANCwW8=.png")
    src = cv2.imread(path)
    cv2.namedWindow("input", 0)
    cv2.resizeWindow("input", 640, 480)
    cv2.imshow("input", src)
    width, height, channel = src.shape
    """
    提取图中的灰色部分
    """
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)  # BGR转HSV
    low_hsv = np.array([1, 0, 24])  # 这里要根据HSV表对应(色相，饱和度，明度)，填入三个min值（表在下面）
    high_hsv = np.array([180, 90, 240])  # 这里填入三个max值
    mask = cv2.inRange(hsv, lowerb=low_hsv, upperb=high_hsv)  # 提取掩膜
    gray_area = np.sum(mask == 255)
    print(gray_area)
    print(width * height)
    # 黑色背景转透明部分
    mask_contrary = mask.copy()
    mask_contrary[mask_contrary == 0] = 1
    mask_contrary[mask_contrary == 255] = 0  # 把黑色背景转白色
    mask_bool = mask_contrary.astype(bool)
    mask_img = cv2.add(src, np.zeros(np.shape(src), dtype=np.uint8), mask=mask)
    # 这个是把掩模图和原图进行叠加，获得原图上掩模图位置的区域
    mask_img = cv2.cvtColor(mask_img, cv2.COLOR_BGR2BGRA)
    mask_img[mask_bool] = [0, 0, 0, 0]
    # 这里如果背景本身就是白色，可以不需要这个操作，或者不需要转成透明背景就不需要这里的操作
    cv2.namedWindow("enhanced", 0);

    cv2.resizeWindow("enhanced", 640, 480);
    cv2.imshow("enhanced", mask_img)
    cv2.imwrite('label123.png', mask_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def test_single_bounds(path,bounds):
    """
    测试用，传入图片路径和弹框区域，可观察弹框位置和掩膜形状，适合单张测试
    返回阴影面积占其他区域的比例
    """
    # src = cv2.imread(r"D:\PythonCode\monkey\deduplicate_result_0402\monkey\com.baidu.haokan\qblpwfcuezdvgnxjsroh_deduplicate\popup_killed\1024inohx.png")
    # src = cv2.imread(r"C:\Users\17180\AppUIAutomator2Navigation\data_819\Images\empty\1VlYIadxaqULVmvb3EjNiVji8u87o6BKWcg5jANCwW8=.png")
    src = cv2.imread(path)

    cv2.namedWindow("input", 0)
    cv2.resizeWindow("input", 640, 480)

    # 把弹框区域涂成白色
    cv2.rectangle(src, (bounds[0], bounds[1]), (bounds[2], bounds[3]), color=(255, 255, 255), thickness=-1)

    cv2.imshow("input", src)

    width, height, channel = src.shape
    """
    提取图中的灰色部分
    """
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)  # BGR转HSV
    low_hsv = np.array([0, 0, 1])  # 这里要根据HSV表对应，填入三个min值（表在下面）
    low_hsv = np.array([0, 0, 20])
    low_hsv = np.array([0, 0, 10])
    high_hsv = np.array([180, 90, 240])
    high_hsv = np.array([180, 120, 240])
    high_hsv =np.array([180, 240, 210]) # 这里填入三个max值
    mask = cv2.inRange(hsv, lowerb=low_hsv, upperb=high_hsv)  # 提取掩膜
    gray_area = np.sum(mask == 255)
    print()
    print(f"灰色区域面积为：{gray_area}")
    all_area = width * height
    print("总面积为："+str(all_area))
    popup_area = (bounds[2] - bounds[0]) * (bounds[3] - bounds[1])
    print(f"弹框面积为：{popup_area}")
    print(f'灰色面积占背景的比例为{gray_area/(all_area-popup_area)}')
    # 黑色背景转透明部分
    mask_contrary = mask.copy()
    mask_contrary[mask_contrary == 0] = 1
    mask_contrary[mask_contrary == 255] = 0  # 把黑色背景转白色
    mask_bool = mask_contrary.astype(bool)
    mask_img = cv2.add(src, np.zeros(np.shape(src), dtype=np.uint8), mask=mask)

    # cv2.namedWindow("masked", 0)
    #
    # cv2.resizeWindow("masked", 640, 480)
    # cv2.imshow("masked", mask)

    # 这个是把掩模图和原图进行叠加，获得原图上掩模图位置的区域
    mask_img = cv2.cvtColor(mask_img, cv2.COLOR_BGR2BGRA)
    mask_img[mask_bool] = [0, 0, 0, 0]
    # 这里如果背景本身就是白色，可以不需要这个操作，或者不需要转成透明背景就不需要这里的操作


    # cv2.namedWindow("enhanced", 0);
    #
    # cv2.resizeWindow("enhanced", 640, 480);
    # cv2.imshow("enhanced", mask_img)
    # cv2.imwrite('label123.png', mask_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def shadow_detect(img_path,bounds):
    '''
    传入图片路径和弹窗范围，返回阴影面积占其他区域的比例，检测阴影主要调用这个函数
    '''
    src = cv2.imread(img_path)
    cv2.rectangle(src,(bounds[0],bounds[1]),(bounds[2],bounds[3]),color=(255,255,255),thickness=-1)
    width, height, channel = src.shape

    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)  # BGR转HSV

    """
    提取图中的灰色部分
    """
    # hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)  # BGR转HSV
    # low_hsv = np.array([0, 0, 1])  # 这里要根据HSV表对应，填入三个min值（表在下面）
    # low_hsv = np.array([0, 0, 20]) # 1
    low_hsv = np.array([0, 0, 10])
    # high_hsv = np.array([180, 90, 240])
    # high_hsv = np.array([180, 120, 240])# 这里填入三个max值
    # high_hsv = np.array([180, 130, 210]) # 1
    high_hsv = np.array([180, 240, 210])
    mask = cv2.inRange(hsv, lowerb=low_hsv, upperb=high_hsv)  # 提取掩膜
    gray_area = np.sum(mask == 255)
    # print(gray_area)
    # print(width * height)
    all_area = width * height
    popup_area = (bounds[2]-bounds[0])*(bounds[3]-bounds[1])
    return gray_area/(all_area-popup_area)

def detect_shadow(image_path, bounds):
    res = shadow_detect(image_path, bounds)
    if res > 0.5:
        return True
    return False