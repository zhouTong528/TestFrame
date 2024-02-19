from common.log import Logger
from py_page.base_page import BasePage

logging = Logger(__name__).get_logger()


# 个人资料页面
class UserCenterPage(BasePage):
    yaml_path = BasePage.get_yaml_path('user_center_page.yaml')

    # 获取用户昵称列表
    def get_user_names(self):
        logging.info('获取用户昵称列表：get_user_names')
        eles = self.run_steps(self.yaml_path, 'get_user_names')
        user_names = [
            ele.text for ele in eles
        ]

        return user_names, self

    # 编辑性别
    def edit_gender(self, gender):
        logging.info(f'编辑性别为{gender}：edit_gender')
        if gender == '女':
            loc = '//span[text()="女"]'
        elif gender == '男':
            loc = '//span[text()="男"]'
        else:
            raise ValueError(f"Invalid gender value: {gender}")
        self.run_steps(self.yaml_path, 'edit_gender', gender=loc)
        return self

    # 获取性别
    def get_gender(self):
        logging.info('获取性别：get_gender')
        ele = self.run_steps(self.yaml_path, 'get_gender')
        logging.info(f'性别为{ele.text}')
        return ele.text, self
