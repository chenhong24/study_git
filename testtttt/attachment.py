import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

"""
QQ mail:smtp.qq.com  port:465

"""
# 连接smtp服务器并登录
smtp = smtplib.SMTP_SSL(host="smtp.qq.com", port=465)
smtp.login(user="953354870@qq.com", password="diivnuvqipwqbdca")

# content = "将结果发送到邮件"
# with open("report1.html","r",encoding="utf8") as f:
#     content = f.read()

msg = MIMEMultipart()
with open("report1.html", "rb") as f:
    content = f.read()


text_msg = MIMEText(content, _subtype="html", _charset="utf8")
msg.attach(text_msg)
report = MIMEApplication(content)
report.add_header('content-disposition', 'attachment', filename='cc.html')
msg.attach(report)

msg["subject"] = "cc"
msg["from"] = "953354870@qq.com"
msg["To"] = ""

smtp.send_message(msg, from_addr="953354870@qq.com", to_addrs="953354870@qq.com")
