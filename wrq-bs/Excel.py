import xlwt
from sql import mysql
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart

subject = ""
text = None
receivers = "948447747@qq.com"
doc_name = ""

# 第三方 SMTP 服务
mail_host = "smtp.163.com"  # 设置服务器
mail_user = "duya_kindle_push@163.com"  # 用户名
mail_pass = "Kindle990126"  # 口令

class mail:
    def __init__(self, doc_name):
        self.message = MIMEMultipart()
        self.message['From'] = "{}".format(mail_user)
        self.message['To'] = ",".join(receivers)
        self.message['Subject'] = doc_name
        self.name = doc_name

    def Enclosure(self):
        # 构造附件1，传送当前目录下的 test.txt 文件
        doc_route = "Excel/" + self.name
        att1 = MIMEText(open(doc_route, 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        att1["Content-Disposition"] = 'attachment; filename=' + self.name
        self.message.attach(att1)

    def send(self):
        self.Enclosure()
        try:
            smtpObj = smtplib.SMTP_SSL(mail_host)
            smtpObj.connect(mail_host, 465)    # sslPort
            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(mail_user, receivers, self.message.as_string())
            return "Success"
        except smtplib.SMTPException:
            return "Error"

def mem2xls(data):
    styleNum = xlwt.easyxf(num_format_str='#,##0.00')# 设置数字型格式为小数点后保留两位
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('new sheet', cell_overwrite_ok=True)
    # 设置表头
    header = ['时间','光强传感器/V', '压力传感器/V']
    for index, k in enumerate(header):
        sheet.write(0, index, k)
    # 数据写入excel
    for index, val in enumerate(data):
        sheet.write(index+1, 0, val['time'])  # 第二行开始
        sheet.write(index+1, 1, round(val['v1'], 2))
        sheet.write(index+1, 2, round(val['v2'], 2))
    xls_name = str(time.strftime("%Y-%m-%d--%H-%M", time.localtime()))+'.xls'
    book.save("Excel/"+xls_name)
    return xls_name