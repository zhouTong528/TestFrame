import json
import os
from random import random
import pytest
from filelock import FileLock
from common.log import Logger


logging = Logger(__name__).get_logger()


@pytest.fixture(scope="session", autouse=True)
def get_token(tmp_path_factory, worker_id):
    if worker_id == "master":
        token = str(random())
        logging.info(f"fixture：请求登录接口，获取token,{token}")
        os.environ['token'] = token
        return token

    root_tmp_dir = tmp_path_factory.getbasetemp().parent
    fn = root_tmp_dir / "data.json"
    with FileLock(str(fn) + ".lock"):

        if fn.is_file():
            token = json.loads(fn.read_text())
            logging.info(f"fixture：读取缓存文件，token是：{token}")
        else:
            token = str(random())
            logging.info(f"fixture：请求登录接口，获取token:{token}")
            # 【不可删除、修改】
            fn.write_text(json.dumps(token))
            logging.info(f"首次执行，token是：{token}")

        # 将后续需要保留的数据存在某个地方，比如这里是os的环境变量
        os.environ['token'] = token
    return token
