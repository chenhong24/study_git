import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from common.handleconfig import conf

"""
QQ mail:smtp.qq.com  port:465

"""


def send_email(filename, title):
    """

    :param filename: 文件路径
    :param title: 邮件的标题
    :return:
    """
    # 连接smtp服务器并登录
    smtp = smtplib.SMTP_SSL(host=conf.get("email", "host"), port=conf.get("email", "port"))
    smtp.login(user=conf.get("email", "user"), password=conf.get("email", "pwd"))

    # content = "将结果发送到邮件"
    # with open("report1.html","r",encoding="utf8") as f:
    #     content = f.read()

    msg = MIMEMultipart()
    with open(filename, "rb") as f:
        content = f.read()

    text_msg = MIMEText(content, _subtype="html", _charset="utf8")
    msg.attach(text_msg)
    report = MIMEApplication(content)
    report.add_header('content-disposition', 'attachment', filename=filename)
    msg.attach(report)

    msg["subject"] = title
    msg["from"] = "953354870@qq.com"
    msg["To"] = ""

    smtp.send_message(msg, from_addr=conf.get("email", "from_addr"),
                      to_addrs=conf.get("email", "to_addrs"))
