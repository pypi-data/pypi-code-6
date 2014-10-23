#!/usr/bin/python
# -*- coding:utf-8 -*-
# This Python file uses the following encoding: utf-8

from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext  # für extra context
from easy_contact.forms import ContactForm
from django.views.decorators.cache import cache_control
import settings

@cache_control(private=True)
def contact(request):
    """
    View für simples Kontaktformular.
    """
    def get_mail():
        """
        Ist App django-contact-form-setup installiert werden die darüber zur verfügung gestellten
        Paramerter verwendet. Sind keine Settings vorzufinden oder ist App nicht
        installiert werden Ersatzparamerter aus User verwendet:
        Generiere Empfänger Email, der erste gefunden Nutzer in der
        Gruppe: "mail_support" wird genommen
        """
        try:
            settings.EMAIL_HOST
        except AttributeError:
            raise AttributeError('Please setup the settings.EMAIL_HOST!')

        if 'easy_contact_setup' in settings.INSTALLED_APPS:
            from easy_contact_setup.models import Setting
            m = Setting.objects.filter(active=True)
            if m:
                d = {}
                d.update({'DEFAULT_FROM_EMAIL' : m[0].to_email})
                d.update({'EMAIL_HOST_PASSWORD' : m[0].email_host_password})
                d.update({'EMAIL_HOST_USER' : m[0].email_host_user})
                return d
        else:
            try:
                d = {}
                d.update({'DEFAULT_FROM_EMAIL' : settings.DEFAULT_FROM_EMAIL})
                d.update({'EMAIL_HOST_PASSWORD' : settings.EMAIL_HOST_PASSWORD})
                d.update({'EMAIL_HOST_USER' : settings.EMAIL_HOST_USER})
                return d
            except AttributeError:
                raise AttributeError('''Pleas configure your settings file with
                                        the necessary mailserver settings.''')
        # Configuration Error
        raise IOError(""""Create in the easy_contact_setup app a setting instance and activate it!""")

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                # Sende mail mit Absendeadresse des Mailformular Benutzers.
                send_mail(
                    subject='Message from %s on website %s' % (cd['email'], request.META['HTTP_HOST']),
                    message='Subj: ' + cd['subject'] + '\n\n' + cd['message'],
                    from_email=cd['email'],  # Absender in Mailformular
                    recipient_list=[
                                    get_mail()['DEFAULT_FROM_EMAIL'],
                                    ],
                    auth_user=get_mail()['EMAIL_HOST_USER'],
                    auth_password=get_mail()['EMAIL_HOST_PASSWORD'],
                    )
            # Sende mail mit eigener Absendeadresse (Maildienste erlauben
            # oft keine fremde Absendeadressen)
            except:
                send_mail(
                    subject='Message from %s on website %s' % (cd['email'], request.META['HTTP_HOST']),
                    message='Subj: ' + cd['subject'] + '\n\n' + cd['message'],
                    from_email=get_mail()['DEFAULT_FROM_EMAIL'],  # Eigene Mailadresse
                    recipient_list=[
                                    get_mail()['DEFAULT_FROM_EMAIL'],
                                    ],
                    auth_user=get_mail()['EMAIL_HOST_USER'],
                    auth_password=get_mail()['EMAIL_HOST_PASSWORD'],
                    )
            return HttpResponseRedirect('/%s/feedback/success/' % request.LANGUAGE_CODE)
    else:
        form = ContactForm(
            initial={'message': ''}
        )

    current_dict = {'form': form, }
    return render_to_response('easy_contact/contact.html', current_dict, context_instance=RequestContext(request))


def thanks(request):
    return render_to_response('easy_contact/success.html', context_instance=RequestContext(request))
