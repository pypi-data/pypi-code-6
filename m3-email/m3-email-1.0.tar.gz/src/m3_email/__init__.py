#coding:utf-8
from m3.helpers import logger
from django.conf import settings
from django.core.mail import get_connection
from django.core.mail.message import EmailMessage
from django.template import loader
from m3.ui.actions.results import OperationResult

from smtplib import SMTPSenderRefused

class EmailProxy(object):
    '''
    Класс, облегчающий работу отправки сообщений
    '''
    
    ADDR_FROM = settings.EMAIL_ADDRESS_FROM
    ADDR_TO = [settings.EMAIL_ADDRESS_TO,]
    
    def __init__(self):
        self.messages = []
        self.connection =  get_connection(
                      auth_user = settings.EMAIL_HOST_USER,
                      auth_password= settings.EMAIL_HOST_PASSWORD)
    
    def add(self, template, template_dict, **kwargs):
        '''
        Добавление писем в стек
        '''
        kwargs['body'] = loader.render_to_string(template, template_dict)        
        kwargs['from_email'] = kwargs.get('from_email', EmailProxy.ADDR_FROM)
        kwargs['to'] = kwargs.get('to', EmailProxy.ADDR_TO)
        msg = EmailMessage(**kwargs)
        msg.content_subtype = "html"
        self.messages.append(msg)
        
    def send(self):
        '''
        Отправка писем
        '''
        if self.messages:
            try:
                self.connection.send_messages(self.messages)
            except SMTPSenderRefused as smtp_exception:
                msg = u'Почтовый сервер перегружен. Попробуйте позже.'
                logger.warning(msg=smtp_exception.message)
                return OperationResult.by_message(msg)
