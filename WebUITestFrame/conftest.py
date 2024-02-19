from time import sleep

import pytest

from common.log import Logger
from common.screen_shot import get_screenshot_gif
from py_page.base_page import BasePage
from py_page.main_page import MainPage
logging = Logger(__name__).get_logger()


@pytest.fixture
def setup_driver():
    init = BasePage()
    driver = init.driver
    yield driver
    get_screenshot_gif()
    driver.quit()


@pytest.fixture(scope='session', autouse=True)
def get_cookies():
    try:
        logging.info(f'执行fixture：get_cookies,获取cookies')
        dr = MainPage().click_login().use_account_password_login('15314824648', '123456789qQ')
        cookies = dr.driver.get_cookies()
        sleep(2)
        dr.driver.quit()
        logging.info(f'获取cookies成功：{cookies}\n')
        return cookies
    except Exception as e:
        logging.error(f'获取cookies失败：{e}')
        return None

