from jsonpath import jsonpath
from common.log import Logger
logging = Logger(__name__).get_logger()


def json_res(json_data: dict, json_path: str, index: int = 0) -> str or list:
    """
    :rtype: object
    :param json_data: json数据
    :param json_path: jsonpath表达式
    :param index: jsonpath匹配结果下标
    :return: jsonpath匹配结果
    """
    matched_result = jsonpath(json_data, json_path)
    logging.info(f'jsonpath匹配结果是: {matched_result}')
    if matched_result and index is not None:
        return matched_result[index]
    elif matched_result and index is None:
        return matched_result
    else:
        raise TypeError('jsonpath 未匹配到数据')
