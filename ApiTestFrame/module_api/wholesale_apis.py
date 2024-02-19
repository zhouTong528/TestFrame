from common.log import Logger
from module_api.base_api import BaseApi

logging = Logger(__name__).get_logger()


class WholesaleApis(BaseApi):

    yaml_path = BaseApi.get_yaml_api_path('wholesale_apis.yaml')

    def submit_wholesale_order_api(self, token, contPerson, goods):
        """
        批发开单接口
        :param token: token
        :param contPerson: 客户信息
        :param goods: 商品信息
        :return:
        """
        logging.info('执行批发开单接口：submit_wholesale_order_api')
        return self.run_requests(self.yaml_path, 'submit_wholesale_order_api', token=token, contPerson=contPerson, goods=goods)

    def get_contPerson_info_api(self, token, cust_name):
        """
        获取客户信息接口
        :param token: token
        :param cust_name: 客户名称
        :return:
        """
        logging.info('执行获取客户信息接口：get_contPerson_info_api')
        return self.run_requests(self.yaml_path, 'get_contPerson_info_api', token=token, cust_name=cust_name)
