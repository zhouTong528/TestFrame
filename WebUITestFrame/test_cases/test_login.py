import allure
import pytest

from common.log import Logger
from py_page.main_page import MainPage
from common.screen_shot import getScreenShot
from common.setup_util import SetupUtil
logging = Logger(__name__).get_logger()

@allure.feature('登录模块')
class TestLogin(SetupUtil):


    @allure.story('正向登录测试用例')
    @allure.title('使用正确的账号密码登录')
    @allure.description('使用账号密码登录测试，进入首页获取登录名称，判断登录是否成功')
    @pytest.mark.smoke
    def test_use_account_password_login(self, setup_driver):
        logging.info('---------------UI自动化开始---------------')
        logging.info('测试用例名称：test_use_account_password_login')

        name = \
        MainPage(setup_driver).click_login().use_account_password_login('15314824648', '123456789qQ').get_login_name()[
            0]
        logging.info('预期结果：测试小周9651')
        logging.info('实际结果：' + name)
        try:
            assert name == '测试小周9651'
            logging.info('账号密码登录成功')
            logging.info('---------------UI自动化结束---------------\n')
        except AssertionError as e:
            getScreenShot(__name__)
            logging.error('账号密码登录失败')
            logging.info('---------------UI自动化结束---------------\n')
            raise e
