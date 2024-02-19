import datetime
import os

import allure
import pyscreenshot as ImageGrab
import time


# 测试用例断言失败截图
def getScreenShot(funcName):
    # 构建文件路径
    formatted_date = datetime.datetime.now().strftime("%Y-%m-%d")
    file_path = os.path.abspath(os.path.join(os.getcwd(), ".", "screen_shot", formatted_date))
    os.makedirs(file_path, exist_ok=True)
    # 构建文件名
    curr_time = time.strftime("%m%d%H%M%S")
    file_name = os.path.join(file_path, f"{funcName}-{curr_time}.png")
    # 获取当前页面的截图
    im = ImageGrab.grab()
    im.save(file_name)
    im.close()
    # 把截图添加到 allure 附件中（测试报告中会带此截图）
    allure.attach.file(source=file_name, name=f'断言失败截图-{funcName}+{curr_time}',
                       attachment_type=allure.attachment_type.PNG)


# 测试用例步骤截图
def get_screenshot_gif():
    # 构建文件路径
    formatted_date = datetime.datetime.now().strftime("%Y-%m-%d")
    file_path = os.path.abspath(os.path.join(os.getcwd(), ".", "screen_gif", formatted_date))
    os.makedirs(file_path, exist_ok=True)

    # 定义截图保存的路径
    curr_time = str(int(time.time() * 1000))
    file_name = os.path.join(file_path, curr_time + '.png')

    with ImageGrab.grab() as im:
        im.save(file_name)


if __name__ == '__main__':
    getScreenShot('test')
