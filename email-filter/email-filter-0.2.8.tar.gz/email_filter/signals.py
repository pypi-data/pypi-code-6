# -*- coding: utf-8 -*-
from django.dispatch import Signal

mail_for_unknown_user = Signal(
    providing_args=[
        "instance", "original_msg", "mail_sender_email", "send_email", "smtp_sendmail"
    ]
)
