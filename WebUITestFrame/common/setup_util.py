import datetime
import glob
import os
import time
import PIL
import allure
import imageio
import numpy as np
from PIL import Image
from common.log import Logger

logging = Logger(__name__).get_logger()


class SetupUtil:

    def teardown_method(self):
        """
        用例执行结束时，将所有截图合并为一个GIF文件
        """
        # 获取所有PNG格式的截图文件
        formatted_date = datetime.datetime.now().strftime("%Y-%m-%d")
        screenshot_dir = os.path.abspath(os.path.join(os.getcwd(), ".", "screen_gif", formatted_date))
        screenshots = glob.glob(os.path.join(screenshot_dir, "*.png"))
        sorted_screenshots = sorted(screenshots)

        frames = []
        for filename in sorted_screenshots:
            with PIL.Image.open(filename) as frame:
                frames.append(np.array(frame))

        # 输出GIF文件路径
        curr_time = str(int(time.time() * 1000))
        output_filename = os.path.join(screenshot_dir, f'{curr_time}.gif')

        try:
            imageio.mimsave(output_filename, frames, format='GIF', duration=800, loop=0)
            allure.attach.file(source=output_filename, name=f'步骤截图动画{output_filename}',
                               attachment_type=allure.attachment_type.PNG)
        except:
            logging.error("GIF文件创建失败")
        finally:
            for img_file in sorted_screenshots:
                os.remove(img_file)
