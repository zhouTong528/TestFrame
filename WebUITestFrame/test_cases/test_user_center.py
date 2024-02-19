import allure
import pytest
from common.log import Logger
from common.screen_shot import getScreenShot
from py_page.main_page import MainPage
from common.setup_util import SetupUtil
logging = Logger(__name__).get_logger()

@allure.feature('个人资料模块')
class TestUserCenter(SetupUtil):

    @allure.story('编辑个人资料用例')
    @allure.title('编辑用户性别')
    @allure.description('编辑用户性别，编辑成功后，再次获取用户性别，验证是否修改成功')
    # 编辑用户信息-性别
    @pytest.mark.function
    @pytest.mark.flaky(rerun=2, reruns_delay=1)
    @pytest.mark.parametrize('set_gender', ['男', '女'])
    def test_edit_user_gender(self, setup_driver,  get_cookies, set_gender):
        logging.info('---------------UI自动化开始---------------')
        logging.info(f'测试用例名称：test_edit_user_gender')
        logging.info(f'使用参数化，本次参数为：{set_gender}')
        dr = MainPage(setup_driver).add_cookies(get_cookies).refresh().goto_personal_center_page(). \
            goto_user_center_page()

        gender = dr.edit_gender(set_gender).get_gender()[0]
        logging.info('预期结果：' + set_gender)
        logging.info('实际结果：' + gender)

        try:
            assert gender == set_gender
            logging.info('测试用例执行成功')
            logging.info('---------------UI自动化结束---------------\n')

        except AssertionError as e:
            getScreenShot(__name__)
            logging.error('测试用例执行失败')
            logging.info('---------------UI自动化结束---------------\n')
            raise e
