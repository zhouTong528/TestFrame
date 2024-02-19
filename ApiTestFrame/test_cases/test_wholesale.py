import allure
import pytest
from common.json_res import json_res
from common.log import Logger
from common.read_yaml import *
from db_datas.db_users_data import DBUsersData
from module_api.wholesale_apis import WholesaleApis

logging = Logger(__name__).get_logger()


@allure.feature("批发模块")
class TestWholesale:

    yaml_datas_path = WholesaleApis.get_yaml_datas_path('test_wholesale.yaml')

    @allure.story('批发开单')
    @allure.title('正向批发开单用例')
    @allure.description('使用张三，和xxx商品进行开单，断言结果正确，及单号是否在db中存在')
    @pytest.mark.smoke
    @pytest.mark.parametrize('datas', get_datas(yaml_datas_path,'test_submit_wholesale_order'),
                             ids=get_ids(yaml_datas_path, "test_submit_wholesale_order"))
    def test_submit_wholesale_order(self,get_token, datas):
        logging.info('---------------接口自动化开始---------------')
        logging.info('测试用例名称：test_submit_wholesale_order')

        wholesale_apis = WholesaleApis()
        # 获取开单业务数据
        cont_person = datas['cont_person']
        cont_person_res = wholesale_apis.get_contPerson_info_api(get_token, cont_person)
        cont_person_data = json_res(cont_person_res, '$..contPerson')

        # 执行开单业务
        goods = datas['goods']
        wholesale_order_res = wholesale_apis.submit_wholesale_order_api(get_token, cont_person_data, goods)
        status_code = wholesale_order_res['status_code']
        msg = wholesale_order_res['msg']
        docNo = json_res(wholesale_order_res, '$..docNo')
        logging.info(f'实际结果：status_code: {status_code}, msg: {msg}, docNo: {docNo}')

        try:
            assert status_code == 200
            assert msg == '提交成功'
            assert docNo != ''
            docNo_list = DBUsersData().get_wholesale_docNo(710)
            logging.info(f'查询到tenID:710的docNo: {docNo_list}')
            assert docNo in docNo_list
            logging.info('接口自动化测试成功')
            logging.info('---------------接口自动化结束---------------\n')
        except AssertionError as e:
            logging.error('接口自动化测试失败')
            logging.info('---------------接口自动化结束---------------\n')
            raise e

