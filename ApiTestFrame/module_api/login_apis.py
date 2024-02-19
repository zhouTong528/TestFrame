from module_api.base_api import BaseApi
from common.log import Logger

logging = Logger(__name__).get_logger()


class LoginApis(BaseApi):
    yaml_path = BaseApi.get_yaml_api_path('login_apis.yaml')

    def login_api(self, username, password):
        """
        登录接口
        :param username: 用户名
        :param password: 密码
        :return: 返回登录接口的响应数据
        """
        logging.info('执行登录接口：login_api')
        res = self.run_requests(self.yaml_path, 'login', account=username, pwd=password)
        logging.info(f"登录账号：{username}，密码：{password}")
        return res

    def register_api(self, username, password):
        """
        注册接口
        :param username: 用户名
        :param password: 密码
        :return: 返回注册接口的响应数据
        """
        logging.info('执行注册接口：register_api')
        res = self.run_requests(self.yaml_path, 'register', account=username, pwd=password)
        logging.info(f"注册账号：{username}，密码：{password}")
        return res
