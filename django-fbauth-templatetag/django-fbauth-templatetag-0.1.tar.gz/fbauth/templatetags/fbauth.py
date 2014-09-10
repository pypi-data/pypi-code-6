# -*- coding:utf-8 -*-
from django import template
from django.template.loader import render_to_string

from .. import constants, settings

register = template.Library()


@register.inclusion_tag('fbauth/css.html')
def fbauth_css():
    return {}


@register.inclusion_tag('fbauth/button.html')
def fbauth_button():
    return dict(
        JQUERY_CDN=constants.JQUERY_CDN,
        JQUERY_REQUIRED_VERSION=constants.JQUERY_REQUIRED_VERSION,
        FACEBOOK_API=constants.FACEBOOK_API.format(
            locale=settings.FBAUTH_FACEBOOK_LOCALE),
        FACEBOOK_APP_ID=settings.FBAUTH_FACEBOOK_APP_ID,
        FBAUTH_REDIRECT_URL=settings.FBAUTH_REDIRECT_URL)
