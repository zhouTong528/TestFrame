from time import sleep

from common.log import Logger
from py_page.base_page import BasePage

logging = Logger(__name__).get_logger()


# 主页
class MainPage(BasePage):
    yaml_path = BasePage.get_yaml_path('main_page.yaml')

    # 点击登录按钮
    def click_login(self):
        logging.info('点击登录按钮：click_login')
        self.run_steps(self.yaml_path, 'click_login')
        return self

    # 使用账户密码登录
    def use_account_password_login(self, account, pwd):
        logging.info('使用账户密码登录：use_account_password_login')
        logging.info(f'登录账号是: {account}，密码是: {pwd}')
        self.run_steps(self.yaml_path, 'use_account_password_login', account=account, pwd=pwd)
        return self

    # 获取登录账号名称
    def get_login_name(self):
        logging.info('获取登录账号名称：get_login_name')
        ele = self.run_steps(self.yaml_path, 'get_login_name')
        login_name = ele.get_attribute("innerText")
        logging.info(f'名称是: {login_name}')
        return login_name, self

    # 进入个人中心页面
    def goto_personal_center_page(self):
        logging.info('进入个人中心页面：goto_personal_center_page')
        self.run_steps(self.yaml_path, 'goto_personal_center_page')
        sleep(2)
        from py_page.personal_center_page import PersonalCenterPage
        return PersonalCenterPage(self.driver)

    # 进入发布文章页面
    def goto_publish_article_page(self):
        logging.info('进入发布文章页面：goto_publish_article_page')
        self.run_steps(self.yaml_path, 'goto_publish_article_page')
        sleep(2)
        from py_page.publish_article_page import PublishArticlePage
        return PublishArticlePage(self.driver)
