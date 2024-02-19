import cv2 as cv
from PIL import Image
import pytesseract
import os
from common.log import Logger

logging = Logger(__name__).get_logger()


def image_recognition(element_png_file, output_directory="./"):
    """
    :param element_png_file: 验证码截图存放的截图路径
    :param output_directory: 输出文件的目录
    :return: 识别到的验证码
    """
    try:
        # 原图
        master_drawing = cv.imread(element_png_file)
        if master_drawing is None:
            logging.error(f"无法读取文件: {element_png_file}")
            return None

        # 对图片进行去噪处理
        denoised_picture = cv.pyrMeanShiftFiltering(master_drawing, 10, 100)

        # 对图片进行灰度处理
        grayscale_picture = cv.cvtColor(denoised_picture, cv.COLOR_BGR2GRAY)

        # 对图片进行二值化处理
        threshold_value, binary_picture = cv.threshold(grayscale_picture, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
        binary_picture_path = os.path.join(output_directory, "binary_picture.png")
        cv.imwrite(binary_picture_path, binary_picture)

        # 使用PIL打开图像转化为图像对象，并使用pytesseract进行图像识别
        with Image.open(binary_picture_path) as captcha_picture:
            verification_code = pytesseract.image_to_string(captcha_picture)

            # 删除二值化后图片
            os.remove(binary_picture_path)
            return verification_code

    except FileNotFoundError:
        logging.error(f"文件未找到: {element_png_file}")

    except pytesseract.TesseractError as e:
        logging.error(f"OCR识别错误: {e}")

    except Exception as e:
        logging.error(f"其他错误: {e}")

    finally:
        return None
