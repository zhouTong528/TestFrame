import os
import traceback
from string import Template
import requests
import yaml
from common.log import Logger

logging = Logger(__name__).get_logger()


class BaseApi:

    def request_api(self, method, api, headers=None, params=None, json=None, data=None, files=None) -> dict:
        """
        发送请求,进行二次封装
        :param method: 请求方法
        :param api: 请求地址
        :param headers: 请求头
        :param params: 请求参数
        :param json: 请求体
        :param data: 请求体
        :param files: 文件
        :return: 返回响应数据字典{'status_code':xxx, 'response':xxx}
        """
        config_data_dict = self.get_config_datas('base_api')
        host = config_data_dict['host']
        timeout = config_data_dict['timeout']

        url = host + api
        response_dict = {}
        if method in ['get', 'GET']:
            try:
                res = requests.get(url=url, params=params, headers=headers, timeout=timeout)
                # 获取响应头，查看返回数据的格式
                res_headers = res.headers
                headers_type = res_headers.get('Content-Type')
                if headers_type == 'application/json':
                    response = res.json()
                else:
                    response = res.text
                # 获取响应码
                status_code = res.status_code
                # 加入response_dict字典返回出去
                response_dict['status_code'] = status_code
                response_dict['response'] = response
                return response_dict
            except Exception as e:
                error_info = traceback.format_exc()
                logging.error(f'接口::{api}请求失败，请求出错::{e}，错误详情::{error_info}')


        elif method in ['post', 'POST']:
            try:
                res = requests.post(url=url, params=params, headers=headers, json=json, data=data, files=files,
                                    timeout=timeout)
                # 获取响应头，查看返回数据的格式
                res_headers = res.headers
                headers_type = res_headers.get('Content-Type')
                if headers_type == 'application/json':
                    response = res.json()
                else:
                    response = res.text
                # 获取响应码
                status_code = res.status_code
                # 加入response_dict字典返回出去
                response_dict['status_code'] = status_code
                response_dict['response'] = response
                return response_dict
            except Exception as e:
                error_info = traceback.format_exc()
                logging.error(f'接口::{api}请求失败，请求出错::{e}，错误详情::{error_info}')

    def run_requests(self, yaml_path, api_name, **kwargs) -> dict:
        """
        执行请求
        :param yaml_path: yaml文件路径
        :param api_name: yaml文件中的api名称
        :param kwargs: 参数
        :return:返回响应数据
        """
        with open(yaml_path, 'r', encoding="UTF-8") as f:
            yaml_datas = yaml.safe_load(f)
        api_datas = yaml_datas.get(api_name)
        # 在不丢失原数据类型描述的基础上转换成字符串
        str_api_datas = yaml.dump(api_datas)
        if kwargs:
            for k in kwargs.keys():
                if isinstance(kwargs[k], str):
                    kwargs[k] = f"'{kwargs[k]}'"
            # 替换参数
            str_api_datas = Template(str_api_datas).substitute(kwargs)
        api_datas = yaml.safe_load(str_api_datas)
        logging.info(f'执行接口::{api_name},传入接口参数::{kwargs},执行接口请求参数::{api_datas}')
        res = self.request_api(**api_datas)
        logging.info(f'接口::{api_name}，返回数据::{res}')
        return res

    @staticmethod
    def get_yaml_api_path(yaml_name) -> str:
        """
        获取api_yaml文件的绝对路径
        :param yaml_file_name: yaml文件名
        :return:yaml文件的绝对路径
        """
        path = os.path.abspath(__file__)
        py_page_path = os.path.dirname(path)
        project_path = os.path.dirname(py_page_path)
        yam_path = os.path.join(project_path, 'module_api_datas', yaml_name)
        return yam_path

    @staticmethod
    def get_yaml_datas_path(yaml_name) -> str:
        """
        获取case_datas_yaml文件的绝对路径
        :param yaml_file_name: yaml文件名
        :return:yaml文件的绝对路径
        """
        path = os.path.abspath(__file__)
        py_page_path = os.path.dirname(path)
        project_path = os.path.dirname(py_page_path)
        yam_path = os.path.join(project_path, 'test_cases_data', yaml_name)
        return yam_path

    @staticmethod
    def project_path() -> str:
        """
        获取项目根目录
        :return:项目根目录
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_path = os.path.dirname(current_dir)
        return project_path

    @staticmethod
    def get_config_datas(key) -> dict:
        """
        读取配置文件
        :return:
        """
        config_path = os.path.join(BaseApi.project_path(), 'config.yaml')
        with open(config_path, 'r', encoding="UTF-8") as f:
            yaml_data = yaml.safe_load(f)
        datas = yaml_data[key]
        return datas


if __name__ == '__main__':
    base_api = BaseApi.get_config_datas('base_api')
    print(base_api)
