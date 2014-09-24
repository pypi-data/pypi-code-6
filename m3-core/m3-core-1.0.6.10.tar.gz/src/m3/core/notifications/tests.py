#coding:utf-8

from django.test import TestCase
from django.core import mail
from m3.core.notifications.email_notifications import *
from django.utils.encoding import smart_unicode

class Dummy:
    pass

class Email_Notification_Test(TestCase):
    
    def test_exceptions(self):
        self.assertRaises(EmailBodyTemplateDoesNotExist, EmailNotify, 'not existed template')
        self.assertRaises(EmailSubjectTemplateDoesNotExist, EmailNotify, 'WithoutSubjectTest.txt')
        hello = TxtMessageTest()
        self.assertRaises(ProfileInformationRequired, hello.Send, Dummy())
        
    def test_sending(self):
        # 1. Проверяем: тип контента, тему, содержание, адрес получателя и доп. словарь
        mail.outbox = []
        txt = TxtMessageTest()
        profile = Dummy()
        profile.email = 'ivan@ivan.com'
        profile.user_name = u'Иван Иванович'
        txt.Send(profile, A =  111, B = 222)
        
        self.failUnlessEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.failUnlessEqual(email.content_subtype, 'plain')
        #TODO: Узнасть что за хренотень добавляется в начало u'\ufeff' ?
        self.failUnlessEqual(email.subject, u'\ufeff' + u'тема сообщения')
        checkMsg = u'Тест тесктового сообщения %s %s %s' % (111, 222, profile.user_name)
        checkMsg = u'\ufeff' + smart_unicode(checkMsg)
        self.failUnlessEqual(email.body, checkMsg)
        self.failUnlessEqual(email.to, ['ivan@ivan.com'])
        
        # 2. Тест массовой рассылки
        mail.outbox = []
        email_list = ['vova@ya.ru', 'sasha@gmail.com', 'tom@cat.local']
        html = HtmlMessageTest()
        html.Send_to_emails(email_list)
        self.failUnlessEqual(len(mail.outbox), len(email_list))
        for ind, email in enumerate(mail.outbox):
            self.failUnlessEqual(email.content_subtype, 'html')
            # Сравниваем списки, т.к. рассылка может быть множеству получателей, но мы рассылаем по одному
            self.failUnlessEqual(email.to, [email_list[ind]]) 


