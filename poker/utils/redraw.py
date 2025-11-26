import cv2
import os

image_folder = "../data_detect/images_origin"
label_folder = "../runs/detect/exp16/labels"
output_folder = "../data_detect/images_detected"

os.makedirs(output_folder, exist_ok=True)

for image_file in os.listdir(image_folder):
    # 提取文件名
    file_name = os.path.splitext(image_file)[0]
    image_path = os.path.join(image_folder, image_file)
    label_path = os.path.join(label_folder, f"{file_name}.txt")

    image = cv2.imread(image_path)

    if os.path.exists(label_path):
        with open(label_path, "r") as f:
            lines = f.readlines()

        for line in lines:
            # 解析YOLO格式位置信息
            values = line.strip().split()
            class_id, cx, cy, w, h, confidence = map(float, values[:6])

            image_height, image_width, _ = image.shape
            left = int((cx - w / 2) * image_width)
            top = int((cy - h / 2) * image_height)
            right = int((cx + w / 2) * image_width)
            bottom = int((cy + h / 2) * image_height)

            # 绘制矩形框
            cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 10)

            # 绘制置信度
            text = f"Confidence: {confidence:.2f}"
            font_scale = 2
            font_thickness = 2
            text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
            text_width, text_height = text_size
            cv2.putText(image, text, (left, top - 10 - text_height), cv2.FONT_HERSHEY_SIMPLEX, font_scale,
                        (0, 0, 255), font_thickness)

    output_image_path = os.path.join(output_folder, f"{file_name}_drawn.jpg")
    cv2.imwrite(output_image_path, image)


