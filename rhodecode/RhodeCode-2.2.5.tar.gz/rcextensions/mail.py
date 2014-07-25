# -*- coding: utf-8 -*-
"""
mail plugin that uses RhodeCode mail config to send an email.

example use in hooks::

    call = load_extension('mail.py')
    if call:
        kwargs = dict()
        kwargs['email_config'] = {...} email dict config
        kwargs['recipients'] = <list of recipients> ['usr1@rhodecode.com', 'foobar@rhodecode.com']
        kwargs['subject'] = <mail subject>
        kwargs['body'] = <body>
        # optional set html body
        kwargs['body_html'] = <html>
        call(**kwargs)

    ## Email config dict variables, only smtp_server is required for min. config
    {
        'smtp_server': 'localhost',
        'smtp_username': '',
        'smtp_password': '',
        'smtp_port': '',
        'smtp_use_tls': False,
        'smtp_use_ssl': False,
        'smtp_auth': '', # LOGIN, PLAIN, CRAM-MD5, etc
        'debug': False, # show debug info when sending emails
    }

"""

def run(*args, **kwargs):
    """
    Extra params that could be passed here

    :param email_config: config of email parameters, one could use a
        rhodecode_tools configObj to parse it like:
        from rhodecode_tools.lib.configobj.configobj import ConfigObj
        conf = ConfigObj(kwargs['config'])['DEFAULT']
        note to propagate original hook ['config'] key which is a path to the
        .ini file. Email config is in DEFAULT section
    :param subject: mail subject
    :param recipients: list of recipients
    :param body: plaintext body
    :param body_html: html body (changes email mimetype also)
    """
    from rhodecode.lib.celerylib import tasks, run_task

    email_config = kwargs.get('email_config')
    recipients = kwargs.get('recipients')
    email_subj = kwargs.get('subject')
    email_body = kwargs.get('body')
    email_body_html = kwargs.get('body_html')

    return run_task(tasks.send_email, recipients, email_subj,
                    email_body, email_body_html, email_config=email_config)
