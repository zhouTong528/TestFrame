import os
import traceback
import yaml
from common.log import Logger
from common.send_email import SendEmail
from common.zip_file import zip_files
from py_page.base_page import BasePage

logging = Logger(__name__).get_logger()


def run_cases():
    with open('config.yaml', mode='r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    logging.info('********************【开始运行测试用例】********************')
    logging.info(f'url地址为：{data["url"]}\n')

    # 运行测试用例
    os.system('pytest -s -q --alluredir=./allure_result --clean-alluredir')
    os.system('allure generate ./allure_result/ -o ./allure_report/ --clean')
    os.system('allure open ./allure_report/')

    # 压缩文件
    source = rf'{BasePage.project_path()}/allure_report'
    destin = rf'{BasePage.project_path()}/allure_report_zip/report.zip'
    res = zip_files(source, destin)

    try:
        if res:
            # 发送邮件
            email_data = data['send_email']
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
