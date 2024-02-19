from db_datas.base_db import BaseDB


class DBUsersData:

    def get_user_mobiles(self):
        """
        查询user表中所有用户手机号
        :return:
        """
        db = BaseDB('user')
        sql = 'select mobile from user'
        db_users = db('select', sql)
        mobiles_list = [user_dict['mobile'] for user_dict in db_users]
        db(connect=False)
        return mobiles_list

    def get_wholesale_docNo(self, tenID):
        """
        查询wholesale表中所有的单号
        :return:
        """
        db = BaseDB('sale')
        sql = f'select docNo from wholesale where tenID = {tenID}'
        db_res = db('select', sql)
        docNo_list = [user_dict['docNo'] for user_dict in db_res]
        db(connect=False)
        return docNo_list
