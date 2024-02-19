import base64
import os
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


class SendEmail:

    # 初始化服务器信息
    def __init__(self, mail_host, mail_user, mail_key, sender, receivers):
        self.mail_host = mail_host
        self.mail_user = mail_user
        self.mail_key = mail_key
        self.sender = sender
        self.receivers = list(receivers)

    # 以文本的形式发送邮件
    def send_email_by_text(self, context, subject, from_address, to_address):
        # QQ邮箱发送者名称是中文则需要base64编码
        from_base64 = base64.b64encode(from_address.encode())
        from_base64 = from_base64.decode()

        message = MIMEText(context, 'plain', 'UTF-8')
        message['Subject'] = subject  # 邮件标题
        message['From'] = f'=?utf-8?B?{from_base64}?= <{self.sender}>'  # 邮件主体中发送者名称
        message['To'] = Header(to_address, "utf-8")  # 邮件主体中接收者名称
        self.__send_email(message)

    # 以文本和附件的形式发送邮件
    def send_email_by_att(self, file_path, from_address, to_address, subject='API接口自动化测试报告',
                          context='自动化测试报告，详情请查看附件'):
        # QQ邮箱发送者名称是中文则需要base64编码
        from_base64 = base64.b64encode(from_address.encode())
        from_base64 = from_base64.decode()
        # 生成包含多个部分的邮件主体对象
        message = MIMEMultipart()
        message['Subject'] = subject  # 邮件标题
        message['From'] = f'=?utf-8?B?{from_base64}?= <{self.sender}>'  # 邮件主体中发送者名称
        message['To'] = Header(to_address, "utf-8")  # 邮件主体中接收者名称
        # 文本内容
        body = MIMEText(context, 'plain', 'utf-8')
        message.attach(body)
        # 附件内容
        att_body = open(file_path, 'rb')  # 以二进制的格式打开附件
        att = MIMEApplication(att_body.read())  # 导入附件
        att_body.close()
        file_name = os.path.split(file_path)[1]
        att.add_header('Content-Disposition', 'attachment', filename=file_name)  # 添加附件名称
        message.attach(att)
        self.__send_email(message)

    # 登录并进行发送
    def __send_email(self, message):
        # 进行登录发送
        try:
            smtpobj = smtplib.SMTP(local_hostname="SB")
            smtpobj.connect(self.mail_host, 25)
            smtpobj.login(self.mail_user, self.mail_key)
            smtpobj.sendmail(self.sender, self.receivers, message.as_string())
            smtpobj.quit()
        except Exception as e:
            raise e


if __name__ == '__main__':
    mail_host = 'smtp.qq.com'  # 发送邮箱的主机域名
    mail_user = 'xx'  # 登录 QQ 邮箱的QQ号
    mail_key = 'xxx'  # 邮箱登录授权码
    sender = '2299xxx@qq.com'  # 发送邮箱地址
    receivers = ['229xxx@qq.com', '1760xxx8@163.com']  # 接收者

    email = SendEmail(mail_host, mail_user, mail_key, sender, receivers)
    email.send_email_by_text('V3.4.0版本已完成系统测试', '测试主题', '测试人', '测试负责人')
