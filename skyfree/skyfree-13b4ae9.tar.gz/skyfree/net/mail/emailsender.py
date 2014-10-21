#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4 et
#
# Copyright @ 2014 OPS, Qunar Inc. (qunar.com)
#
# Author: tingfang.bao <tingfang.bao@qunar.com>
# DateTime: 14-7-22 下午4:22

import smtplib
from email.mime.text import MIMEText


# noinspection PyMethodMayBeStatic
class EmailSender():
    def __init__(self, smtp_server):
        self.smtp_server = smtp_server

    def send_mail(self, sender, to_list, subject, html_content):
        """

        :param sender: 发送地址
        :param to_list: 收件邮件列表
        :param subject: 主题
        :param html_content: 邮件内容
        :return: 是否发送成功
        """
        msg = MIMEText(html_content, "html", "UTF-8")
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ";".join(to_list)
        try:
            smtp = smtplib.SMTP()
            smtp.connect(self.smtp_server)
            smtp.sendmail(sender, to_list, msg.as_string())
            smtp.close()
            return True
        except Exception, e:
            print str(e)
            return False
