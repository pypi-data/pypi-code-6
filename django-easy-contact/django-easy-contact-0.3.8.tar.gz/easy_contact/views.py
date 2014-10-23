#!/usr/bin/python
# -*- coding:utf-8 -*-
# This Python file uses the following encoding: utf-8

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext  # für extra context
from easy_contact.forms import ContactForm
from django.views.decorators.cache import cache_control
import settings

# We will use smtplib and email instead of django.core.mail. That because we
# can easely get the mail host from database instead of the settings file and
# that without modify djangos core mail.
# There is a bug in smtp lib, so if you run it on a development server it may
# not work as you expect. For more Information see:
# http://stackoverflow.com/questions/383738/104-connection-reset-by-peer-socket-error-or-when-does-closing-a-socket-resul
import smtplib
from smtplib import SMTPException
from email.mime.text import MIMEText


@cache_control(private=True)
def contact(request):
    """
    View für simples Kontaktformular.
    1. It should be possible to us the contact form by give only the reciver adress
    in the django-contac-formt-setup so the server in settings.py will be used
    for sending.
    2. If a full server setup is given in django-contac-formt-setup than it will
    be used
    3. if Complete server setup is not installed then settings.py is used for
    complete mail host setup.

    Anyway, for best results use a smtp server who allowed to send mails with any
    sender adress.
    """
    def get_mail_data():
        """
        If django-contac-formt-setup is installed than get data set from the app if not
        pull it from settings.py
        Also if there are missig data in spite of no server was specified in
        the app than it will be filled up by our setup.py
        """
        # our error message if not enought data available.
        error_message = 'Pleas configure your settings file withthe necessary mailserver settings.'
        d = {}  # dataset

        # Sending with the senders from email we can only try if a complete server setup.
        # is given. Only a mail adress is not enough. In this case we use the
        # from the settings.py.
        send_with_formulars_email_from = False  # so later we will care about this variabls

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

            # skip settings.py only if all parameters avallible
            if m.mail_host and m.mail_host_pass and m.mail_host_user:
                send_with_formulars_email_from = True
                return d, send_with_formulars_email_from
            else:
                # this will used as sender address if send_with_formulars_email_from
                # is False
                d['MAIL_FROM'] = settings.DEFAULT_FROM_EMAIL

        # else if easy_contact_setup isn't installed then get data from setup.py
        else:
            send_with_formulars_email_from = True
            try:
                d['MAIL_DEFAULT_TO'] = settings.DEFAULT_FROM_EMAIL
            except AttributeError:
                raise AttributeError(error_message)

        # now get ste smtp setup data if not got before
        try:
            d['MAIL_HOST_PASS'] = settings.EMAIL_HOST_PASSWORD
            d['MAIL_HOST_USER'] = settings.EMAIL_HOST_USER
            d['MAIL_HOST'] = settings.EMAIL_HOST
            return d, send_with_formulars_email_from
        except AttributeError:
            # our error message if not enought data available.
            raise AttributeError(error_message)

    # Handle Post data and send the email
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # first fetch data from database/settings.py and form
            sd, swmd = get_mail_data()
            cd = form.cleaned_data

            # and then create the data set from cleaned post data
            subject = u'Message from %s on website %s' % (cd['email'], request.META['HTTP_HOST'])
            message = u'Subj: %s\n\n%s' % (cd['subject'], cd['message'])
            mail_from = cd['email']  # Absender in Mailformular

            # recipient list may be extendet in future versions
            mail_recipient_list = [sd['MAIL_DEFAULT_TO'], ]

            def get_mime_text_instance(subj=subject, mail_from=mail_from, mail_to=sd['MAIL_DEFAULT_TO']):
                """Create and configure an mime text instance"""
                inst = MIMEText(message.encode('utf-8'), 'plain', 'UTF-8')
                inst['Subject'] = subj
                inst['From'] = mail_from
                inst['To'] = mail_to
                return inst

            # Smtp login
            s = smtplib.SMTP(sd['MAIL_HOST'])
            try:
                s.login(sd['MAIL_HOST_USER'], sd['MAIL_HOST_PASS'])
            except SMTPException:
                s.starttls()
                s.ehlo()
                s.login(sd['MAIL_HOST_USER'], sd['MAIL_HOST_PASS'])

            # Sending the Mail
            if swmd:
                try:
                    # Send mail with the sender adress of the mail form user.
                    msg = get_mime_text_instance()
                    s.sendmail(msg['From'], mail_recipient_list, msg.as_string())
                except smtplib.SMTPSenderRefused:
                    # ups that worked not very well, now we try a different
                    # sender adress.
                    # Now We send with the own default email adress as sender
                    # adress - email services often do not allow to send an
                    # email with a foreign email address.

                    # we create a new MIMEText instance and configure it again (the
                    # old works not anymore)
                    msg = get_mime_text_instance(mail_from=sd['MAIL_DEFAULT_TO'])

                    # and now sending the mail again
                    s.sendmail(msg['From'], mail_recipient_list, msg.as_string())
            else:
                # Here we use all server data from the settings.py except the
                # recivers adress (it comes from the app)
                msg = get_mime_text_instance(mail_from=sd['MAIL_FROM'])
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
