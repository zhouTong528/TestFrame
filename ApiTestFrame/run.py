import os
import random
import subprocess

import yaml

from common.log import Logger
from common.send_email import SendEmail
from common.zip_file import zip_files
from module_api.base_api import BaseApi

logging = Logger(__name__).get_logger()
def run_cases():
    with open('config.yaml', 'r', encoding='utf-8') as f:
        datas = yaml.safe_load(f)
    base_api = datas['base_api']
    host = base_api['host']
    timeout = base_api['timeout']

    logging.info('********************【开始运行测试用例】********************')
    logging.info(f'运行host地址：{host}，设置超时时间：{timeout}秒\n')

    # 运行
    os.system('pytest -s -q --alluredir=./allure_result --clean-alluredir -n 2')
    os.system('allure generate ./allure_result/ -o ./allure_report/ --clean')
    os.system('allure open ./allure_report/')

    # 压缩文件
    source = rf'{BaseApi.project_path()}/allure_report'
    destin = rf'{BaseApi.project_path()}/allure_report_zip/report.zip'
    res = zip_files(source, destin)

    try:
        if res:
            # 发送邮件
            email_data = datas['send_email']
            send_email = SendEmail(**email_data)
            send_email.send_email_by_att(destin, 'Test-zhouTong', 'Leader')
            logging.info('测试报告邮件发送成功')
            logging.info('********************【测试用例运行结束】********************\n')
    except Exception as e:
        # print(traceback.format_exc())
        logging.error(f'测试报告邮件发送失败，错误是：{e}')
        logging.info('********************【测试用例运行结束】********************\n')
        raise e





if __name__ == '__main__':
    run_cases()