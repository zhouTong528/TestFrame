import os
import sys
import time
from string import Template

import pyautogui
import pyperclip
import yaml
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from common.handle_black import handle_black
from common.log import Logger
from common.screen_shot import get_screenshot_gif

logging = Logger(__name__).get_logger()


class BasePage:

    def __init__(self, driver=None):
        if driver is None:
            driver_path = os.path.join(BasePage.project_path(), 'driver_version/chromedriver.exe')
            service = Service(driver_path)
            # 下载路径
            download_dir = os.path.join(BasePage.project_path(), 'download')
            options = webdriver.ChromeOptions()
            prefs = {'profile.default_content_settings.popups': 0,  # 禁止弹出窗口
                     "profile.default_content_setting_values.automatic_downloads": 1,  # 允许自动下载
                     'download.default_directory': download_dir
                     }
            options.add_experimental_option('prefs', prefs)

            if sys.platform.startswith('win'):
                self.driver = webdriver.Chrome(service=service, options=options)
            else:
                self.driver = webdriver.Remote(command_executor='http://172.20.10.2:4444/wd/hub', options=options)

            ####
            self.driver.maximize_window()
            self.driver.implicitly_wait(10)

            config_path = os.path.join(BasePage.project_path(), 'config.yaml')
            with open(config_path, mode='r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            url = config.get('url')
            self.driver.get(url)

            get_screenshot_gif()
        else:
            self.driver = driver

    @handle_black
    def find(self, by, locator):
        """
        :param by: 定位方式
        :param locator: 定位器
        :return: 返回元素
        """
        by_locators = {
            'id': (By.ID, locator),
            'class': (By.CLASS_NAME, locator),
            'name': (By.NAME, locator),
            'css': (By.CSS_SELECTOR, locator),
            'xpath': (By.XPATH, locator),
            'link_text': (By.LINK_TEXT, locator),
            'partial_link_text': (By.PARTIAL_LINK_TEXT, locator),
            'tag': (By.TAG_NAME, locator)
        }
        by_locator = by_locators.get(by.lower())
        ele = WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element(*by_locator), message="元素超时未找到")
        return ele

    @handle_black
    def find_and_click(self, by, locator):
        self.find(by, locator).click()
        get_screenshot_gif()

    @handle_black
    def find_and_send_keys(self, by, locator, keys):
        self.find(by, locator).send_keys(keys)
        get_screenshot_gif()

    @handle_black
    def find_and_clear(self, by, locator):
        self.find(by, locator).clear()
        get_screenshot_gif()

    @handle_black
    def finds(self, by, locator):
        """
        :param by: 定位方式
        :param locator: 定位器
        :return: 返回元素
        """
        by_locators = {
            'id': (By.ID, locator),
            'class': (By.CLASS_NAME, locator),
            'name': (By.NAME, locator),
            'css': (By.CSS_SELECTOR, locator),
            'xpath': (By.XPATH, locator),
            'link_text': (By.LINK_TEXT, locator),
            'partial_link_text': (By.PARTIAL_LINK_TEXT, locator),
            'tag': (By.TAG_NAME, locator)
        }
        by_locator = by_locators.get(by.lower())
        eles = WebDriverWait(self.driver, 10).until(lambda driver: driver.find_elements(*by_locator), message="元素超时未找到")
        return eles

    @handle_black
    def finds_and_click(self, by, locator, index):
        self.finds(by, locator)[index].click()
        get_screenshot_gif()

    @handle_black
    def finds_and_send_keys(self, by, locator, keys, index):
        self.finds(by, locator)[index].send_keys(keys)
        get_screenshot_gif()

    @handle_black
    def finds_and_clear(self, by, locator, index):
        self.finds(by, locator)[index].clear()
        get_screenshot_gif()

    @handle_black
    def move_to_element(self, by, locator, index=None):
        """
        :param by: 定位方式
        :param locator: 定位器
        :param index: 索引
        :return:
        """
        if index is None:
            ele = self.find(by, locator)
        else:
            ele = self.finds(by, locator)[index]
        ActionChains(self.driver).move_to_element(ele).perform()
        get_screenshot_gif()

    @handle_black
    def switch_to_window(self, index):
        """
        句柄切换窗口
        :param index: 窗口索引
        :return:
        """
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[index])

    @handle_black
    def switch_to_frame(self, frame_identifier):
        """
        切换到指定iframe
        :param frame_identifier: iframe的id、name
        :return:
        """
        self.driver.switch_to.frame(frame_identifier)

    @handle_black
    def switch_to_content(self, target='default_content'):
        """
        切换到指定内容或框架，支持'parent_frame'和'default_content'两种模式
        """
        switcher = {
            'parent_frame': self.driver.switch_to.parent_frame,
            'default_content': self.driver.switch_to.default_content,
        }
        if target in switcher:
            switcher[target]()
        else:
            raise ValueError(f"不支持的目标 '{target}'，请使用'parent_frame'或'default_content'")

    @handle_black
    def switch_alert_and_action(self, yes_or_not=None, text=None):
        """
        处理alert
        :param yes_or_not: 1:yes 0:no
        :param text: 输入文本
        :return:
        """
        alert = self.driver.switch_to.alert
        if text:
            alert.send_keys(text)
            get_screenshot_gif()

        if yes_or_not == 1:
            alert.accept()
        else:
            alert.dismiss()

    @handle_black
    def scroll_page(self, x, y, t=0):
        """
        :param x: 滑动距离x
        :param y: 滑动距离y
        :param t: 滑动时间
        :return:
        """
        ActionChains(self.driver).scroll_by_amount(x, y).pause(t).perform()
        get_screenshot_gif()

    def upload_file(self, path):
        """
        :param path: 文件路径
        :return:
        """
        # 检查path是否存在
        if not os.path.exists(path):
            raise FileNotFoundError(f"找不到文件或文件夹: {path}")
        time.sleep(2)
        # 防止有中文路径,使用pyperclip复制路径
        pyperclip.copy(path)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        pyautogui.press('enter', 2)  # 按2次回车键（按2次是为了防止出错）
        time.sleep(5)
        get_screenshot_gif()

    def add_cookies(self, cookies):
        """
        :param cookies: cookie字典
        :return:
        """
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        time.sleep(2)
        return self

    def refresh(self):
        """
        刷新页面
        :return:
        """
        self.driver.refresh()
        get_screenshot_gif()
        time.sleep(2)
        return self

    def run_steps(self, file_path, operation, **kwargs):
        """
        执行yaml文件中的步骤
        :param file_path: yaml文件的绝对路径
        :param operation: 方法名
        :param kwargs: 其他参数
        :return:
        """
        # 读取yaml文件
        with open(file_path, "r", encoding="UTF-8") as f:
            res = yaml.safe_load(f)
        steps = res.get(operation)
        yaml_str_steps = yaml.dump(steps)

        # 处理kwargs，防止丢失数据类型
        for k in kwargs.keys():
            if isinstance(kwargs[k], str):
                kwargs[k] = f"'{kwargs[k]}'"
        steps = Template(yaml_str_steps).substitute(kwargs)

        # 执行步骤
        steps = yaml.safe_load(steps)
        for step in steps:
            action = step["action"]
            locator = step["locator"]
            index = step["index"]
            text = step["text"]
            sleep_time = step.get("sleep")

            if sleep_time:
                time.sleep(sleep_time)
                logging.info(f"{action}:{locator}定位元素前，进行强制等待时间为:{sleep_time}")

            if action == 'find':
                try:
                    ele = self.find(*locator)
                    logging.info(f"调用 find 方法，定位器是:{locator}")
                    return ele
                except Exception as e:
                    logging.error(f"路径：{file_path}，执行功能是:{operation}，调用方法是:{action}，定位器是:{locator}，定位元素失败，错误信息：{e}")
                    raise e

            elif action == 'find_and_click':
                try:
                    self.find_and_click(*locator)
                    logging.info(f"调用 find_and_click 方法，定位器是:{locator}")
                except Exception as e:
                    logging.error(f"路径：{file_path}，执行功能是:{operation}，调用方法是:{action}，定位器是:{locator}，定位元素失败，错误信息：{e}")
                    raise e

            elif action == 'find_and_send_keys':
                try:
                    self.find_and_send_keys(*locator, keys=text)
                    logging.info(f"调用 find_and_send_keys 方法，定位器是:{locator}，输入文本是:{text}")
                except Exception as e:
                    logging.error(f"路径：{file_path}，执行功能是:{operation}，调用方法是:{action}，定位器是:{locator}，定位元素失败，错误信息：{e}")
                    raise e

            elif action == 'find_and_clear':
                try:
                    self.find_and_clear(*locator)
                    logging.info(f"调用 find_and_clear 方法，定位器是:{locator}")
                except Exception as e:
                    logging.error(f"路径：{file_path}，执行功能是:{operation}，调用方法是:{action}，定位器是:{locator}，定位元素失败，错误信息：{e}")
                    raise e

            elif action == 'finds':
                try:
                    eles = self.finds(*locator)
                    logging.info(f"调用 finds 方法，定位器是:{locator}")
                    return eles
                except Exception as e:
                    logging.error(f"路径：{file_path}，执行功能是:{operation}，调用方法是:{action}，定位器是:{locator}，定位元素失败，错误信息：{e}")
                    raise e

            elif action == 'finds_and_click':
                try:
                    self.finds_and_click(*locator, index=index)
                    logging.info(f"调用 finds_and_click 方法，定位器是{locator}, 下标是{index}")
                except Exception as e:
                    logging.error(
                        f"路径：{file_path}，执行功能是:{operation}，调用方法是:{action}，定位器是:{locator}，下标是{index}，定位元素失败，错误信息：{e}")
                    raise e

            elif action == 'finds_and_send_keys':
                try:
                    self.finds_and_send_keys(*locator, keys=text, index=index)
                    logging.info(f"调用 finds_and_send_keys 方法，定位器是:{locator}, 下标是:{index}, 输入文本是:{text}")
                except Exception as e:
                    logging.error(
                        f"路径：{file_path}，执行功能是:{operation}，调用方法是:{action}，定位器是:{locator}，下标是:{index}，输入文本是:{text}，"
                        f"定位元素失败，错误信息：{e}")
                    raise e

            elif action == 'finds_and_clear':
                try:
                    self.finds_and_clear(*locator, index=index)
                    logging.info(f"调用 finds_and_clear 方法，定位器是:{locator}, 下标是:{index}")
                except Exception as e:
                    logging.error(
                        f"路径：{file_path}，执行功能是:{operation}，调用方法是:{action}，定位器是:{locator}，下标是:{index}，定位元素失败，错误信息：{e}")
                    raise e

            elif action == 'move_to_element':
                try:
                    self.move_to_element(*locator, index=index)
                    logging.info(f"调用 move_to_element 方法，定位器是:{locator}, 下标是:{index}")
                except Exception as e:
                    logging.error(
                        f"路径：{file_path}，执行功能是:{operation}，调用方法是:{action}，定位器是:{locator}，下标是:{index}，定位元素失败，错误信息：{e}")
                    raise e

            elif action == 'switch_to_window':
                try:
                    self.switch_to_window(index=index)
                    logging.info(f"调用 switch_to_window 方法，下标是:{index}")
                except Exception as e:
                    logging.error(
                        f"路径：{file_path}，执行功能是:{operation}，调用方法是:{action}，窗口下标是:{index}，切换窗口失败，错误信息：{e}")
                    raise e

            elif action == 'switch_to_frame':
                try:
                    self.switch_to_frame(frame_identifier=text)
                    logging.info(f"调用 switch_to_frame 方法，目标是:{text}")
                except Exception as e:
                    logging.error(
                        f"路径：{file_path}，执行功能是:{operation}，调用方法是:{action}，切换frme框架是:{text}，切换frame框架失败，错误信息：{e}")
                    raise e

            elif action == 'switch_to_content':
                try:
                    self.switch_to_content(target=text)
                    logging.info(f"调用 switch_to_content 方法，目标是:{text}")
                except Exception as e:
                    logging.error(
                        f"路径：{file_path}，执行功能是:{operation}，调用方法是:{action}，切换框架到:{text}，切换失败，错误信息：{e}")
                    raise e

            elif action == 'switch_alert_and_action':
                try:
                    self.switch_alert_and_action(yes_or_not=index, text=text)
                    logging.info(f"调用 switch_alert_and_action 方法，yes_or_not是:{index}, 输入的text是:{text}")
                except Exception as e:
                    logging.error(
                        f"路径：{file_path}，执行功能是:{operation}，调用方法是:{action}，yes_or_not是:{index}, 输入的text是:{text}，"
                        f"失败，错误信息：{e}")
                    raise e

            elif action == 'scroll_page':
                try:
                    self.scroll_page(*index)
                    logging.info(f"调用 scroll_page 方法，页面滚动是:{index}")
                except Exception as e:
                    logging.error(f"路径：{file_path}，执行功能是:{operation}，调用方法是:{action}，页面是:{index}，滚动页面失败，错误信息：{e}")
                    raise e

            elif action == 'upload_file':
                try:
                    self.upload_file(path=text)
                    logging.info(f"调用 upload_file 方法，上传文件路径是:{text}")
                except Exception as e:
                    logging.error(f"路径：{file_path}，执行功能是:{operation}，调用方法是:{action}，上传文件路径是:{text}，上传文件失败，错误信息：{e}")
                    raise e

            elif action == 'refresh':
                try:
                    self.refresh()
                    logging.info(f"调用 refresh 方法，刷新页面")
                except Exception as e:
                    logging.error(f"路径：{file_path}，执行功能是:{operation}，调用方法是:{action}，刷新页面失败，错误信息：{e}")
                    raise e


    @staticmethod
    def get_yaml_path(yaml_file_name):
        """
        获取yaml文件的绝对路径
        :param yaml_file_name: yaml文件名
        :return:
        """
        path = os.path.abspath(__file__)
        py_page_path = os.path.dirname(path)
        project_path = os.path.dirname(py_page_path)
        yam_path = os.path.join(project_path, 'py_yaml', yaml_file_name)
        return yam_path

    @staticmethod
    def project_path():
        """
        获取项目根目录
        :return:
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_path = os.path.dirname(current_dir)
        return project_path
