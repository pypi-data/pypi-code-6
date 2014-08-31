# -*- coding: utf-8 -*-
from pytasks import App, Infinite
from datetime import datetime as dt
from datetime import timedelta as td
from time import sleep
#关于发邮件的packages
import smtplib
from email.mime.text import MIMEText
def sche_gen():
    # today = dt(2014, 8, 30) #8-30
    today = dt.now()
    time = today
    while 1:
        time += td(seconds=8)
        print time
        yield time

def send_mail(sub,content):
#要发给谁，这里发给1个人
    mailto_list=["hospital_test@163.com"]

    mail_host="smtp.qq.com"
    mail_user="562837353@qq.com"
    mail_pass="uefgsigw"
    mail_postfix="qq.com"
    '''''
    to_list:发给谁
    sub:主题
    content:内容
    send_mail("aaa@126.com","sub","content")
    '''
    me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content,_charset='gbk')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(mailto_list)
    s = smtplib.SMTP()
    s.connect(mail_host)
    s.login(mail_user,mail_pass)
    s.sendmail(me, mailto_list, msg.as_string())
    s.close()



class SendMail:
    def __init__(self):
        self.content = "now: %s"
        self.times = Infinite
        self._sche_gen = sche_gen()
    def schedule(self):
        return self._sche_gen.next()
    def __call__(self):
        try:
            print 'start send an email', dt.now()
            send_mail('test', self.content%(dt.now()))
            print 'sent an email'
        except Exception, e:
            print e
if __name__=='__main__':
    task = SendMail()
    app = App()
    app.add(task)
    app.run()
