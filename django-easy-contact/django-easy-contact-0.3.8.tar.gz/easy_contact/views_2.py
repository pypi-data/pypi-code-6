#!/usr/bin/python
# -*- coding:utf-8 -*-
# This Python file uses the following encoding: utf-8

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext  # für extra context
from easy_contact.forms import ContactForm
from django.views.decorators.cache import cache_control
import settings

# We use smtplib and email instead of django.core.mail. That because we can
# easely get the mail host from database instead of the settings file and that
# without modify the djangos core mail.
# There is a bug in smtp lib, so if you run it on a development server it may
# not work as you expect. For more Information see:
# http://stackoverflow.com/questions/383738/104-connection-reset-by-peer-socket-error-or-when-does-closing-a-socket-resul
import smtplib
from email.mime.text import MIMEText

@cache_control(private=True)
def contact(request):
    """
    View für simples Kontaktformular.
    """
    def get_mail_data():
        """
        If django-contac-formt-setup is installed than get data set from the app if not
        pull it from settings.py
        """
        d = {}  # dataset
        # if installed get data from the easy_contact_setup app
        if 'easy_contact_setup' in settings.INSTALLED_APPS:
            from easy_contact_setup.models import Setup
            try:
                m = Setup.objects.filter(active=True)[0]  # choose the first active object
            except IndexError:
                # if no object is activ than give a hint to set on up
                raise IndexError('Create an instance in the easy_contact_setup app a and activate it!')
            d['MAIL_DEFAULT_TO'] = m.mail_to
            d['MAIL_HOST_PASS'] = m.mail_host_pass
            d['MAIL_HOST_USER'] = m.mail_host_user
            d['MAIL_HOST'] = m.mail_host
            return d

        # else if easy_contact_setup isn't installed then get data from setup.py
        else:
            try:
                d['MAIL_DEFAULT_TO'] = settings.DEFAULT_FROM_EMAIL
                d['MAIL_HOST_PASS'] = settings.EMAIL_HOST_PASSWORD
                d['MAIL_HOST_USER'] = settings.EMAIL_HOST_USER
                d['MAIL_HOST'] = settings.EMAIL_HOST
                return d
            except AttributeError:
                # our error message if not enought data available.
                raise AttributeError('Pleas configure your settings file withthe necessary mailserver settings.')

    # Handle Post data and send the email
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # first fetch data from database/settings.py and form
            setup_data = get_mail_data()
            cd = form.cleaned_data

            # and then create the data set from cleaned post data
            subject = u'Message from %s on website %s' % (cd['email'], request.META['HTTP_HOST'])
            message = u'Subj: %s\n\n%s' % (cd['subject'], cd['message'])
            mail_from = cd['email']  # Absender in Mailformular

            # create the data set from database/settings.py
            mail_default_to = setup_data['MAIL_DEFAULT_TO']
            mail_recipient_list = [mail_default_to, ]
            mail_host = setup_data['MAIL_HOST']
            mail_host_user = setup_data['MAIL_HOST_USER']
            mail_host_pass = setup_data['MAIL_HOST_PASS']

            # So now we create and configure an mime text instance
            msg = MIMEText(message.encode('utf-8'), 'plain', 'UTF-8')
            msg['Subject'] = subject
            msg['From'] = mail_from
            msg['To'] = mail_default_to

            # Smtp login
            s = smtplib.SMTP(mail_host)
            s.login(mail_host_user, mail_host_pass)

            # Sending the Mail
            try:
                # Send mail with the sender adress of the mail form user.
                s.sendmail(msg['From'], mail_recipient_list, msg.as_string())
                s.quit()
            except smtplib.SMTPSenderRefused:
                # ups that worked not very well, we now try a different
                # sender adress.
                # We send with the own default email adress as sender adress - email
                # services often do not allow to send an email with a foreign
                # email address.

                # we create a new MIMEText instance and configure it again (the
                # old works not anymore)
                msg = MIMEText(message.encode('utf-8'), 'plain', 'UTF-8')
                msg['Subject'] = subject
                msg['From'] = mail_default_to  # change the sender
                msg['To'] = mail_default_to

                # and now sending the mail again
                s.sendmail(msg['From'], mail_recipient_list, msg.as_string())
                s.quit()

            return HttpResponseRedirect('/%s/feedback/success/' % request.LANGUAGE_CODE)
    else:
        form = ContactForm(
            # here we can initialize the form with a message
            initial={'message': ''}
        )

    current_dict = {'form': form, }
    return render_to_response('easy_contact/contact.html', current_dict, context_instance=RequestContext(request))


def thanks(request):
    return render_to_response('easy_contact/success.html', context_instance=RequestContext(request))
