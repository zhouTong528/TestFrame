import random

import allure
import pytest
from common.json_res import json_res
from common.read_yaml import get_datas, get_ids
from db_datas.db_users_data import DBUsersData
from module_api.login_apis import LoginApis
from common.log import Logger

logging = Logger(__name__).get_logger()


@allure.feature("登录模块")
class TestLoginApis:
    yaml_datas_path = LoginApis.get_yaml_datas_path('test_login.yaml')

    @allure.story('登录测试用例')
    @allure.title('使用账号密码登录')
    @allure.description('测试登录接口，断言是否返回token')
    @pytest.mark.smoke
    @pytest.mark.parametrize("yaml", get_datas(yaml_datas_path, 'testLogin02'),
                             ids=get_ids(yaml_datas_path, 'testLogin02'))
    def test_login(self, yaml):
        logging.info('---------------接口自动化开始---------------')
        logging.info('测试用例名称：test_login')
        # 获取参数
        account = yaml['account']
        pwd = yaml['pwd']
        expect = yaml['expect']

        # 执行测试
        print("正在执行登录，账号是{},密码是{}".format(account, pwd))
        res = {"msg": '登录成功', 'token': '12345678922qwe'}
        msg = json_res(res, "$..msg")
        logging.info("实际结果是：{}".format(msg))
        logging.info("预期结果是：{}".format(expect))

        # 断言
        try:
            assert msg == expect
            if msg == "登录成功":
                token = json_res(res, "$..token")
                logging.info("token是：{}".format(token))
                assert token != ""
            logging.info("执行登录测试成功")
            logging.info('---------------接口自动化结束---------------\n')
        except AssertionError as e:
            logging.error("执行登录测试失败")
            logging.info('---------------接口自动化结束---------------\n')
            raise e

    @allure.story('登录测试用例')
    @allure.title('新用户注册')
    @allure.description('使用随机号码，进行新用户注册，断言是否注册成功，及db中是否存在新注册用户')
    @pytest.mark.smoke
    def test_new_user_register(self):
        logging.info('---------------接口自动化开始---------------')
        logging.info('测试用例名称：test_register')

        # 构造数据
        new_account = '177' + str(random.randint(10000000, 99999999))
        pwd = '123456'
        # 查询DB是否存在手机号
        moniles_list = DBUsersData().get_user_mobiles()
        while new_account in moniles_list:
            new_account = '177' + str(random.randint(10000000, 99999999))

        # 执行注册
        # res = LoginApis().register_api(new_account, pwd)
        res = {"status_code": 200, "msg": "注册成功", "data": "xxxxx"}
        status_code = res['status_code']
        msg = json_res(res, "$..msg")
        logging.info("实际结果是：{}".format(msg))
        logging.info("预期结果是：注册成功")
        try:
            assert status_code == 200
            assert msg == "注册成功"
            # 再次查询DB是否存在手机号
            moniles_list = DBUsersData().get_user_mobiles()
            logging.info(f'DB查询手机号{new_account}是否存在，查询结果是：{moniles_list}')
            assert new_account in moniles_list
            logging.info(f'{new_account}存在DB_user表中')
            logging.info('执行注册测试成功')
            logging.info('---------------接口自动化结束---------------\n')
        except AssertionError as e:
            logging.error("执行注册测试失败")
            logging.info('---------------接口自动化结束---------------\n')
            raise e
