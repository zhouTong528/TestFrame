from time import sleep

from common.log import Logger
from py_page.base_page import BasePage

logging = Logger(__name__).get_logger()


# 用户中心页面
class PersonalCenterPage(BasePage):
    yaml_path = BasePage.get_yaml_path('personal_center_page.yaml')

    # 点击编辑资料，并切换到编辑窗口 -> 个人资料页面
    def goto_user_center_page(self):
        logging.info('点击编辑资料，进入个人资料页面：goto_user_center_page')
        self.run_steps(self.yaml_path, 'goto_user_center_page')
        sleep(2)
        from py_page.user_center_page import UserCenterPage
        return UserCenterPage(self.driver)
