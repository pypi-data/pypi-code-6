#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
用来作为接受log传递的agent
通过udp通道。
"""

import json
import logging
import logging.config
import SocketServer
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formatdate

logger = logging.getLogger('flylog')


class FlyLogAgent(object):
    debug = False

    def __init__(self, config=None, debug=None):
        self.config = config
        if debug is not None:
            self.debug = debug

    def _configure_mail_host(self):
        mail_client = None

        if self.config.MAIL_USE_SSL:
            mail_client = smtplib.SMTP_SSL(self.config.MAIL_SERVER, self.config.MAIL_PORT)
        else:
            mail_client = smtplib.SMTP(self.config.MAIL_SERVER, self.config.MAIL_PORT)

        mail_client.set_debuglevel(int(self.debug))

        if self.config.MAIL_USE_TLS:
            mail_client.starttls()

        if self.config.MAIL_USERNAME and self.config.MAIL_PASSWORD:
            mail_client.login(self.config.MAIL_USERNAME, self.config.MAIL_PASSWORD)

        return mail_client

    def handle_message(self, message, address):
        recv_dict = json.loads(message)

        role_list = recv_dict.get('role_list')

        if role_list is None:
            # 如果role_list为null，就代表走默认的receiver_list
            mail_receiver_list = self.config.MAIL_RECEIVER_LIST
        else:
            # 否则配置了什么就是什么
            mail_receiver_list = []
            for role, receiver_list in getattr(self.config, 'MAIL_ROLE_TO_RECEIVER_LIST', dict()).items():
                if role in role_list:
                    mail_receiver_list.extend(receiver_list)

            mail_receiver_list = list(set(mail_receiver_list))

        if not mail_receiver_list:
            # 如果没有接收者，就直接返回了
            return

        mail_msg = MIMEText(recv_dict.get('content'), 'plain', 'utf-8')
        mail_msg['Subject'] = Header(u'[%s]Attention!' % recv_dict.get('source'), 'utf-8')
        mail_msg['From'] = self.config.MAIL_SENDER
        mail_msg['To'] = ', '.join(self.config.MAIL_RECEIVER_LIST)
        mail_msg['Date'] = formatdate()

        # 发邮件
        mail_client = self._configure_mail_host()
        mail_client.sendmail(self.config.MAIL_SENDER, mail_receiver_list, mail_msg.as_string())
        mail_client.quit()

    def run(self, host, port):
        class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):
            def handle(sub_self):
                message = sub_self.request[0]
                try:
                    self.handle_message(message, sub_self.client_address)
                except:
                    logger.error('exc occur.', exc_info=True)

        server = SocketServer.ThreadingUDPServer((host, port), ThreadedUDPRequestHandler)

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        except:
            logger.error('exc occur.', exc_info=True)
