import logging
import time
import os


class Logger:

    def __init__(self, name, log_level="INFO", st_level="INFO", file_level="INFO"):
        # 创建记录器logger，并设置等级
        self.__logger = logging.getLogger(name)
        self.__logger.setLevel(log_level)  # log总等级默认设置:INFO，小于等级不会记录
        fmt = logging.Formatter('%(asctime)s - %(filename)s:[%(lineno)s] - [%(levelname)s] - %(message)s')

        ch = logging.StreamHandler()
        curr_path = os.path.abspath(__file__)
        dir_common = os.path.dirname(curr_path)
        dir_frame = os.path.dirname(dir_common)
        log_file = dir_frame + '\\Logs\\'

        # 按年_月_日_时获取当前时间 例如：”2023-04-02“，拼接.log，做文件名
        log_name = time.strftime('%y-%m-%d') + '.log'
        # 拼接路径 = 把文件夹路径 + 文件名
        file_path = log_file + log_name
        fh = logging.FileHandler(file_path, 'a', encoding='UTF-8')

        ch.setFormatter(fmt)
        fh.setFormatter(fmt)

        ch.setLevel(st_level)
        fh.setLevel(file_level)

        # 把handler添加到logger对象中
        self.__logger.addHandler(ch)
        self.__logger.addHandler(fh)

    def get_logger(self):
        return self.__logger


if __name__ == '__main__':
    logger = Logger(__name__).get_logger()
    # log总等级:info , 控制台等级:info , 文件等级:info
    logger.info('INFo')
    logger.debug('debug')
