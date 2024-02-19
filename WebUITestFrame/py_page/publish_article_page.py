from time import sleep

import pyperclip

from common.log import Logger
from py_page.base_page import BasePage
import pyautogui

logging = Logger(__name__).get_logger()


# 发布文章页
class PublishArticlePage(BasePage):
    yaml_path = BasePage.get_yaml_path('publish_article_page.yaml')

    # 上传图片
    def upload_image(self, path):
        logging.info('开始上传图片：upload_image')
        logging.info('上传图片路径：' + path)
        self.run_steps(self.yaml_path, 'upload_image', path=path)
        return self

    # 获取上传图片元素
    def get_upload_image_element(self):
        logging.info('开始获取上传图片元素：get_upload_image_element')
        ele = self.run_steps(self.yaml_path, 'get_upload_image_element')
        return ele, self

