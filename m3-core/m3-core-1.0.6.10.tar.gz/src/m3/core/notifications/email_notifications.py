# -*- coding: utf-8 -*-
'''
Модуль предоставляет средства для отправки писем с использованием шаблонов.

По умолчанию шаблоны берутся из DEFAULT_MAIL_TEMPLATES_PATH пакета, но этот путь может быть переопределен
добавлением в настройки проекта (settings.py) константы MAIL_TEMPLATES_PATH. В этом случае происк
производится в первую очередь по этому пути.
Шаблон каждого письма состоит из шаблона тела и шаблона заголовка, которые содержат в себе текст или
HTML вперемежку с тегами шаблонов Django. Заголовок письма имеет то же имя что и тело письма, но 
имеет расширение .subject. При отправке они рендерятся и формируют письмо.

Базовый класс реализующий отправку - EmailNotify. Каждое оповещение должно быть его наследником.

Для работы почты в settings.py необходимо задать настройки EMAIL_HOST, EMAIL_HOST_USER, MAIL_HOST_PASSWORD
(смотри справку по настройкам http://docs.djangoproject.com/en/1.1/ref/settings/#ref-settings)

Пример использования:
  u = HtmlMessageTest()
  u.Send(profile)
  u.Send_to_emails(['vova@qwerty.ru', 'pasha@dot.com'])
  Так же к методу Send и Send_to_emails можно добавлять словарь с дополнительными данными для рендеринга
'''

from django.template import TemplateDoesNotExist
from django.template.context import Context
from django.conf import settings
from os import path
from django.template.loader import get_template_from_string
from django.core.mail import EmailMessage, SMTPConnection


DEFAULT_MAIL_TEMPLATES_PATH = 'default_mail_templates' 
DEFAULT_NOTIFY_EMAIL_ADDRESS = 'admin@localhost.local'

#=================================== ИСКЛЮЧЕНИЯ ===================================
class EmailBodyTemplateDoesNotExist(Exception):
    pass
    
class EmailSubjectTemplateDoesNotExist(Exception):
    pass

class ProfileInformationRequired(Exception):
    pass

#============================ ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ =============================
def load_mail_template_from_storage(templateName):
    ''' Возвращает экземпляр Template созданный из почтового шаблона '''
    # Если задан путь к собственным шаблонам, то ищем сначала в нём
    if hasattr(settings, 'MAIL_TEMPLATE_FOLDER'):
        full_name = path.join(settings.MAIL_TEMPLATE_FOLDER, templateName)
        if path.isfile(full_name):
            line = open(full_name).read()
            return get_template_from_string(line)

    # Если шаблон не найден или путь не задан, то пробуем загрузить типовой шаблон
    full_name = path.join(path.dirname(__file__), DEFAULT_MAIL_TEMPLATES_PATH, templateName)
    if path.isfile(full_name):
        line = open(full_name).read()
        return get_template_from_string(line)
    else:
        raise TemplateDoesNotExist()


#============================= КЛАССЫ СООБЩЕНИЙ ==================================

class EmailNotify():
    ''' Базовый класс реализующий отправку письма пользователю '''
    
    def __init__(self, templateName):
        '''
        profile - Профиль пользователя. Из него берутся имя и почтовый адрес
        templateName - Имя файла шаблона
        kwargs - Словарь дополнительных данных для рендеринга шаблона
        '''
        assert isinstance(templateName, str), 'Имя шаблона должно быть строкой'
        assert len(templateName) > 0
        
        # Загрузка шаблона письма
        try:
            self._template = load_mail_template_from_storage(templateName)
        except TemplateDoesNotExist:
            raise EmailBodyTemplateDoesNotExist(templateName)
        
        # Загрузка шаблона темы письма
        try:
            self._subject_template = load_mail_template_from_storage(self._getSubjectTemplateName(templateName))
        except TemplateDoesNotExist:
            raise EmailSubjectTemplateDoesNotExist(templateName)
        
        self._conn = SMTPConnection()
        self._mime_type = self._getMIMEtype(templateName)
    
    def _getMIMEtype(self, templateName):
        ''' Определяет MIME тип шаблона по расширению '''
        dotIndex = templateName.rindex('.')
        if dotIndex > 0:
            ext = templateName[dotIndex + 1:].lower()
            if (ext == 'html') or (ext == 'htm'):
                return 'html'
        return 'plain'
    
    def _getSubjectTemplateName(self, templateName):
        ''' Возвращает имя шаблона темы письма по имени шаблона тела письма '''
        dotIndex = templateName.rindex('.')
        if dotIndex > 0:
            templateName = templateName[:dotIndex]
        templateName += '.subject'
        return templateName
    
    def _prepareContext(self, profile, **kwargs):
        context = Context();
        if profile:
            # Заполняем поля контекста из профиля пользователя
            if not hasattr(profile, 'user_name'):
                raise ProfileInformationRequired('Не задано имя профиля')
            if not hasattr(profile, 'email'):
                raise ProfileInformationRequired('Не задан почтовый адрес пользователя')
            context['user_name'] = profile.user_name
            context['user_email'] = profile.email
        # Адрес отправителя
        try:
            context['sender_email'] = settings.NOTIFY_EMAIL_ADDRESS
        except AttributeError:
            context['sender_email'] = DEFAULT_NOTIFY_EMAIL_ADDRESS
        # Прочие необходимые для конкретного варианта значения передаются через **kwargs
        context.update(kwargs)
        # Рендерим письмо
        message = self._template.render(context)
        subject = self._subject_template.render(context)
        return (subject, message, context)
    
    def Send(self, profile, **kwargs):
        '''
        Отправляет письмо пользователю по адресу из профиля
        profile - Профиль пользователя. Из него берутся имя и почтовый адрес
        kwargs - Словарь дополнительных данных для рендеринга шаблона
        '''
        subject, message, context = self._prepareContext(profile, **kwargs)
        #Отправка письма
        mail = EmailMessage(subject, message, context['sender_email'], 
                            [context['user_email']], connection = self._conn)
        mail.content_subtype = self._mime_type
        mail.send()
    
    def Send_to_emails(self, emails, **kwargs):
        '''
        Отправляет письмо по заданным адресам
        emails - список почтовых адресов
        kwargs - Словарь дополнительных данных для рендеринга шаблона
        '''
        assert isinstance(emails, list) or isinstance(emails, tuple)
        subject, message, context = self._prepareContext(None, **kwargs)
        for address in emails:
            mail = EmailMessage(subject, message, context['sender_email'],
                                [address], connection = self._conn)
            mail.content_subtype = self._mime_type
            mail.send()
            
class TxtMessageTest(EmailNotify):
    def __init__(self):
        EmailNotify.__init__(self, 'TxtMessageTest.txt')

class HtmlMessageTest(EmailNotify):
    def __init__(self):
        EmailNotify.__init__(self, 'HtmlMessageTest.html')
        

