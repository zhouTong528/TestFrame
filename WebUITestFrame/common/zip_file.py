import os
import zipfile
from common.log import Logger

logging = Logger(__name__).get_logger()


def zip_files(source_dir, output_zip_path):
    """
    压缩文件夹函数
    :param source_dir: 需要压缩的文件夹地址
    :param output_zip_path: 压缩后输出的zip文件地址
    :return: 压缩成功返回压缩后的文件地址，压缩失败返回None
    """

    try:
        # 创建ZipFile对象并设置压缩模式
        with zipfile.ZipFile(output_zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            # 遍历源目录下的所有文件和子目录
            for dirpath, dirnames, filenames in os.walk(source_dir):
                # 计算相对路径
                relative_path = dirpath.replace(source_dir, '')
                if relative_path:
                    relative_path += os.sep

                # 将每个文件添加到zip文件中
                for filename in filenames:
                    abs_file_path = os.path.join(dirpath, filename)
                    arcname = os.path.join(relative_path, filename)
                    zipf.write(abs_file_path, arcname=arcname)

        logging.info(f"压缩成功！！！文件夹 {source_dir} 已成功压缩为 {output_zip_path}")
        return output_zip_path
    except Exception as e:
        logging.error(f"压缩文件夹 {source_dir} 失败，错误：{e}")
        return None

if __name__ == '__main__':
    source = './allure_report'
    destin = '../allure_report_zip/report.zip'
    zip_files(source, destin)