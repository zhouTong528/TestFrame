import os
import pymysql
import yaml
from typing import Optional, Dict


class BaseDB:

    def __init__(self, database):
        config_file = os.path.join(os.getcwd(), 'config.yaml')
        # 读取config.yaml中的数据，获取数据库链接信息
        with open(config_file, 'r', encoding='UTF-8') as f:
            datas = yaml.safe_load(f)
        db_data = datas.get('db_data')
        # 链接数据库
        self.connect = pymysql.connect(**db_data, database=database)

    def select_db(self, sql: str) -> dict:
        # 创建游标，并返回的数据是字典的形式
        cursor = self.connect.cursor(pymysql.cursors.DictCursor)
        # sql查询
        cursor.execute(sql)
        db_dats = cursor.fetchall()
        # 关闭游标链接
        cursor.close()
        return db_dats

    def charge_db(self, sql: str) -> None:
        cursor = self.connect.cursor()
        cursor.execute(sql)
        # 提交事务
        self.connect.commit()
        cursor.close()

    def close_db_connect(self) -> None:
        self.connect.close()

    def __call__(self, action: str = None, sql: str = None, connect: bool = True) -> Optional[Dict]:
        if connect:
            if action in ['select', 'SELECT']:
                datas = self.select_db(sql)
                return datas
            elif action in ["UPDATE", "update", "INSERT", "insert", "DELETE", "delete"]:
                self.charge_db(sql)
        else:
            self.close_db_connect()


if __name__ == '__main__':
    pass
