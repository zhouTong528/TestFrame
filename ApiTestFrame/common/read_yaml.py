import yaml

"""
读取yaml文件，作为测试用例数据驱动
"""


def get_datas(yaml_path: str, case_name: str) -> dict:
    """
    :param yaml_path: yaml文件路径
    :param case_name: 测试用例名称
    :return: 测试用例数据
    """
    with open(yaml_path, 'r', encoding='utf-8') as f:
        yaml_datas = yaml.safe_load(f)
    case_datas = yaml_datas[case_name]
    return case_datas


def get_ids(yaml_path: str, case_name: str) -> list:
    """
    :param yaml_path: yaml文件路径
    :param case_name: 测试用例名称
    :return: 测试用例数据ids
    """
    with open(yaml_path, 'r', encoding='utf-8') as f:
        yaml_datas = yaml.safe_load(f)
    case_datas = yaml_datas[case_name]
    ids = [item['name'] for item in case_datas]
    return ids


if __name__ == '__main__':
    path = r'D:\十九\Desktop\测开教程\git框架\ApiTestFrame\test_cases_data\test_login.yaml'
    print(get_datas(path, 'testLogin02'))
