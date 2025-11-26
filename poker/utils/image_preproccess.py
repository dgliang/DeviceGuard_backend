import cv2 as cv
import os
import numpy as np

class ImageProcessor:
    def enhance_edge(self, image):
        # 边缘检测
        blurred = cv.GaussianBlur(image, (3, 3), 0)
        gray = cv.cvtColor(blurred, cv.COLOR_RGB2GRAY)
        edge_output = cv.Canny(gray, 50, 150)
        dst = cv.bitwise_and(image, image, mask=edge_output)
        return dst

    def enhance_contrast(self, image, brightness_factor, contrast_factor):
        # 调整亮度
        brightened = cv.convertScaleAbs(image, alpha=brightness_factor)
        # 调整对比度
        lab = cv.cvtColor(brightened, cv.COLOR_BGR2LAB)
        lab_planes = list(cv.split(lab))
        clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        lab_planes[0] = clahe.apply(lab_planes[0])
        lab = cv.merge(lab_planes)
        contrasted = cv.cvtColor(lab, cv.COLOR_LAB2BGR)
        return contrasted

    # def process_images_dir(self, brightness_factor=1, contrast_factor=1.5):
    #     if not os.path.exists(self.output_dir):
    #         os.makedirs(self.output_dir)
    #
    #     for filename in os.listdir(self.input_dir):
    #         if filename.endswith('.jpg') or filename.endswith('.png'):
    #             image_path = os.path.join(self.input_dir, filename)
    #             image = cv.imread(image_path)
    #
    #             image_canny = self.enhance_edge(image)
    #
    #             kernel = np.ones((1,1), np.uint8)
    #             image_canny = cv.erode(image_canny, kernel)
    #
    #             output_image = self.enhance_contrast(image_canny, brightness_factor, contrast_factor)
    #
    #             output_path = os.path.join(self.output_dir, filename)
    #             cv.imwrite(output_path, output_image)

    def process_image(self, image_path, brightness_factor=1, contrast_factor=1.5):
        if not os.path.exists(image_path):
            print(f"Error: File '{image_path}' not found.")
            return None

        output_dir = os.path.dirname(image_path)
        processed_dir = os.path.join(output_dir, "processed")
        if not os.path.exists(processed_dir):
            os.makedirs(processed_dir)

        filename = os.path.basename(image_path)
        output_path = os.path.join(processed_dir, filename)

        image = cv.imread(image_path)

        image_canny = self.enhance_edge(image)
        kernel = np.ones((1, 1), np.uint8)
        image_canny = cv.erode(image_canny, kernel)

        output_image = self.enhance_contrast(image_canny, brightness_factor, contrast_factor)

        cv.imwrite(output_path, output_image)
        # print(f"Processed image saved at '{output_path}'")
        return output_path

# image_path = r"D:\popUpRecognition-master\test\test_1\00700002.jpg"
#
# processor = ImageProcessor(image_path)
# processor.process_image(brightness_factor=1, contrast_factor=1.5)

