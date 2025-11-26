import cv2
import argparse
import os
import shutil
import numpy as np
import time
import torch
from PIL import Image
from models.yolo import attempt_load
from utils.image_preproccess import ImageProcessor
from utils.datasets import LoadStreams, LoadImages
from utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path
from utils.plots import plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized

def get_button_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default='best.pt', help='model.pt path(s)')
    parser.add_argument('--source', type=str, default='data/images', help='source')  # file/folder, 0 for webcam
    parser.add_argument('--img-size', type=int, default=640, help='inference size (pixels)')
    parser.add_argument('--conf-thres', type=float, default=0.15, help='object confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='IOU threshold for NMS')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true', help='display results')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
    parser.add_argument('--nosave', action='store_true', help='do not save images/videos')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --class 0, or --class 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--update', action='store_true', help='update all models')
    parser.add_argument('--project', default='runs/detect', help='save results to project/name')
    parser.add_argument('--name', default='exp', help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
    opt = parser.parse_args()

    return opt

def get_border_opt():
    parser = argparse.ArgumentParser()
    # parser.add_argument('--weights', nargs='+', type=str, default=ROOT / 'yolov5s.pt', help='model path or triton URL')
    # parser.add_argument('--source', type=str, default=ROOT / 'data/images', help='file/dir/URL/glob/screen/0(webcam)')
    # parser.add_argument('--data', type=str, default=ROOT / 'data/coco128.yaml', help='(optional) dataset.yaml path')
    parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[640], help='inference size h,w')
    # parser.add_argument('--conf-thres', type=float, default=0.25, help='confidence threshold')
    parser.add_argument('--conf-thres', type=float, default=0.75, help='confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='NMS IoU threshold')
    parser.add_argument('--max-det', type=int, default=1000, help='maximum detections per image')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true', help='show results')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
    parser.add_argument('--save-csv', action='store_true', help='save results in CSV format')
    parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
    parser.add_argument('--save-crop', action='store_true', help='save cropped prediction boxes')
    parser.add_argument('--nosave', action='store_true', help='do not save images/videos')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --classes 0, or --classes 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--visualize', action='store_true', help='visualize features')
    parser.add_argument('--update', action='store_true', help='update all models')
    # parser.add_argument('--project', default=ROOT / 'runs/detect', help='save results to project/name')
    parser.add_argument('--name', default='exp', help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
    parser.add_argument('--line-thickness', default=3, type=int, help='bounding box thickness (pixels)')
    parser.add_argument('--hide-labels', default=False, action='store_true', help='hide labels')
    parser.add_argument('--hide-conf', default=False, action='store_true', help='hide confidences')
    parser.add_argument('--half', action='store_true', help='use FP16 half-precision inference')
    parser.add_argument('--dnn', action='store_true', help='use OpenCV DNN for ONNX inference')
    parser.add_argument('--vid-stride', type=int, default=1, help='video frame-rate stride')
    opt = parser.parse_args()
    opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand

    return opt



def get_model(weights_path):
    # 指定使用的GPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # 加载模型
    # weights = 'best_button.pt'  # 更新权重文件路径
    # weights = 'best_borderv1.0.pt'  # 更新权重文件路径
    weights = weights_path
    model = attempt_load(weights, device=device)

    # 将模型设置为评估模式
    model.eval()
    stride = int(model.stride.max())  # model stride
    names = model.module.names if hasattr(model, 'module') else model.names

    return device, model, names

def has_edge(cnt,gray):
    x, y, w, h = cv2.boundingRect(cnt)
    border_intensity = []
    if y > 0:
        border_intensity.append(np.mean(gray[y-1, x:x+w]))
    if y+h+1 < gray.shape[0]:
        border_intensity.append(np.mean(gray[y+h+1, x:x+w]))
    if x > 0:
        border_intensity.append(np.mean(gray[y:y+h, x-1]))
    if x+w+1 < gray.shape[1]:
        border_intensity.append(np.mean(gray[y:y+h, x+w+1]))
    edge_intensity = np.mean(gray[y:y+h, x:x+w]) - np.mean(border_intensity)
    if edge_intensity > 5:
        return True
    return False

def detect_color(cnt,img):
    x, y, w, h = cv2.boundingRect(cnt)
    xmin, ymin, xmax, ymax = x, y, x+w, y+h
    region = img[ymin:ymax, xmin:xmax]
    sobelx = cv2.Sobel(region, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(region, cv2.CV_64F, 0, 1, ksize=5)
    gradient = np.sqrt(sobelx**2.0 + sobely**2.0)
    region_variance = np.var(gradient)
    background = np.copy(img)
    background[ymin:ymax, xmin:xmax] = 0
    sobelx = cv2.Sobel(background, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(background, cv2.CV_64F, 0, 1, ksize=5)
    gradient = np.sqrt(sobelx**2.0 + sobely**2.0)
    background_variance = np.var(gradient)
    # 比较模糊度
    if region_variance - background_variance > 1/5 * background_variance:
        return True
    else:
        mask = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
        mask[y:y+h, x:x+w] = 1
        region_intensity = np.mean(cv2.mean(img, mask=mask))
        mask_inv = cv2.bitwise_not(mask)
        outside_region_intensity = np.mean(cv2.mean(img, mask=mask_inv))
        # 比较颜色亮度
        if region_intensity - outside_region_intensity > 50:
            return True
        return False

def is_center(cnt,img):
    x, y, w, h = cv2.boundingRect(cnt)
    center_x, center_y = x + w//2, y + h//2
    if center_x > img.shape[1] * 0.4 and center_x < img.shape[1] * 0.6 and center_y > img.shape[0] * 0.35 and center_y < img.shape[0] * 0.6:
        return True
    return False

def is_pop(cnt,img,gray):
    x, y, w, h = cv2.boundingRect(cnt)
    # 对区域大小进行限制
    if w!=img.shape[1] and h!=img.shape[0] and w>img.shape[1] * 0.5 and h>img.shape[0] * 0.1 and h < img.shape[0] * 0.9:
        if is_center(cnt,img) and has_edge(cnt,gray) and detect_color(cnt,img):
            return True
    return False

def detect_popup_by_canny(img_path):
    img = cv2.imread(img_path,cv2.IMREAD_UNCHANGED)
    if img is None:
        print("img is None")
        return []
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(img, 100, 200)
    edges = cv2.dilate(edges, None)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    popup_boxes = []
    for cnt in contours:
        if is_pop(cnt,img,gray):
            x, y, w, h = cv2.boundingRect(cnt)
            popup_boxes.append((x, y, x+w, y+h))
    return popup_boxes

def detect_popup_by_yolo(img_path):
    pop_ups = []
    # 预处理
    # processor = ImageProcessor()
    # output_path = processor.process_image(img_path)
    dataset = LoadImages(img_path)

    opt = get_border_opt()
    device, model, names = get_model('best_borderv2.0.pt')
    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(device).float()
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)
        pred = model(img)[0]
        pred = non_max_suppression(pred, opt.conf_thres, opt.iou_thres, classes=opt.classes, agnostic=opt.agnostic_nms)
        for i, det in enumerate(pred):
            if len(det):
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0s.shape).round()
                for *xyxy, conf, cls in reversed(det):
                    box = (int(xyxy[0].item()), int(xyxy[1].item()), int(xyxy[2].item()), int(xyxy[3].item()))
                    # pop_ups.append({"class": names[int(cls)], "bounds": box})
                    pop_ups.append(box)
                    # # YOLO形式的相对坐标
                    # image_height, image_width, _ = im0s.shape
                    # x_center = (xyxy[0].item() + xyxy[2].item()) / (2 * image_width)
                    # y_center = (xyxy[1].item() + xyxy[3].item()) / (2 * image_height)
                    # width = (xyxy[2].item() - xyxy[0].item()) / image_width
                    # height = (xyxy[3].item() - xyxy[1].item()) / image_height
                    # yolo_relative_coords = (x_center, y_center, width, height)
                    # pop_ups.append(yolo_relative_coords)
        return pop_ups

def detect_popup(img_path):
    # 选择用canny或yolo识别弹窗外框
    # popup_boxes = detect_popup_by_canny(img_path)
    # if len(popup_boxes)>0:
    #     # 一个弹窗可能会得到多个轮廓，只取最外层的
    #     box = popup_boxes[0]
    #     return {"class":"pop_up","bounds": box}

    popup_boxes = detect_popup_by_yolo(img_path)

    if len(popup_boxes)>0:
        # 一个弹窗可能会得到多个轮廓，只取最外层的
        box = popup_boxes[0]
        return {"class":"pop_up","bounds": box}
    return None

def detect_button(img_path):
    buttons = []
    dataset = LoadImages(img_path)
    opt = get_button_opt()
    device, model, names = get_model('best_button.pt')
    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(device).float()
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)
        pred = model(img)[0]
        pred = non_max_suppression(pred, opt.conf_thres, opt.iou_thres, classes=opt.classes, agnostic=opt.agnostic_nms)
        for i, det in enumerate(pred):
            if len(det):
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0s.shape).round()
                for *xyxy, conf, cls in reversed(det):
                    box = (int(xyxy[0].item()), int(xyxy[1].item()), int(xyxy[2].item()), int(xyxy[3].item()))
                    buttons.append({"class": names[int(cls)], "bounds": box})
                    # # YOLO形式的相对坐标
                    # image_height, image_width, _ = im0s.shape
                    # x_center = (xyxy[0].item() + xyxy[2].item()) / (2 * image_width)
                    # y_center = (xyxy[1].item() + xyxy[3].item()) / (2 * image_height)
                    # width = (xyxy[2].item() - xyxy[0].item()) / image_width
                    # height = (xyxy[3].item() - xyxy[1].item()) / image_height
                    # yolo_relative_coords = (x_center, y_center, width, height)
                    # buttons.append({"class": names[int(cls)], "bounds": yolo_relative_coords})
        return buttons

def detect_pic(img_path):
    pop_up = detect_popup(img_path)
    if pop_up is None:
        return None
    else:
        buttons = detect_button(img_path)
        res = []
        res.append(pop_up)
        res.extend(buttons)
        return res

# # 使用yolo形式坐标绘图
# def draw_bounding_boxes(image_path, detections,output_folder):
#
#     image = cv2.imread(image_path)
#     filename = os.path.basename(img_path)
#
#     if detections != None:
#         for detection in detections:
#             # 获取类别和边界框坐标
#             cx, cy, w, h = detection['bounds']
#             print(cx,cy,w,h)
#
#             image_height, image_width, _ = image.shape
#             left = int((cx - w / 2) * image_width)
#             top = int((cy - h / 2) * image_height)
#             right = int((cx + w / 2) * image_width)
#             bottom = int((cy + h / 2) * image_height)
#
#             if detection['class'] == "pop_up":
#                 cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 10)
#             else:
#                 cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 10)
#
#     # cv2.imshow('Detected Objects', image)
#     # cv2.waitKey(0)
#     # cv2.destroyAllWindows()
#
#     output_image_path = os.path.join(output_folder, f"{filename}_drawn.jpg")
#     cv2.imwrite(output_image_path, image)


if __name__ == '__main__':
    # src_dir = './all'
    # src_dir = r'E:\下载\popUpRecognition-master\popUpRecognition-master\data_train\Images'
    # output_folder = r'C:\Users\nekoloving\Desktop\output_5'
    src_dir = r'C:\Users\DELL\Downloads\popup\popup'
    img_list = os.listdir(src_dir)
    for file in img_list:
        img_path = os.path.join(src_dir,file)
        res = detect_pic(img_path)
        # draw_bounding_boxes(img_path,res,output_folder)
        print(res)
