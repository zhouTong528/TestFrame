import allure
import pytest

from common.log import Logger
from common.screen_shot import getScreenShot
from common.setup_util import SetupUtil
from py_page.main_page import MainPage

logging = Logger(__name__).get_logger()


@allure.feature('发布文章模块')
class TestPublishArticle(SetupUtil):

    @allure.story('上传图片用例')
    @allure.title('上传5M以下图片')
    @allure.description('上传5M以下图片，上传后查看图片元素是否显示，断言是否成功')
    # 测试上传图片小于5MB
    @pytest.mark.function
    @pytest.mark.flaky(rerun=2, reruns_delay=1)
    def test_upload_image(self, setup_driver, get_cookies):
        logging.info('---------------UI自动化开始---------------')
        logging.info(f'测试用例名称：test_upload_image')

        path = r"D:\十九\Desktop\Selenium.png"
        ele = MainPage(setup_driver).add_cookies(get_cookies).refresh().goto_publish_article_page(). \
            upload_image(path=path).get_upload_image_element()
        try:
            assert ele[0].is_displayed()
            logging.info('上传图片元素可见，测试用例执行成功')
            logging.info('---------------UI自动化结束---------------\n')
        except AssertionError as e:
            getScreenShot(__name__)
            logging.error('上传图片元素不可见，测试用例执行失败')
            logging.info('---------------UI自动化结束---------------\n')
            raise e
