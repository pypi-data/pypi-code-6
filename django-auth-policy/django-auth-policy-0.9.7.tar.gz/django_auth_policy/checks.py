from django.core.urlresolvers import reverse, resolve
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core import checks

from django_auth_policy.user_admin import StrictUserAdmin
from django_auth_policy.admin import (LoginAttemptAdmin, admin_login,
                                      admin_password_change)
from django_auth_policy.forms import (StrictAuthenticationForm,
                                      StrictPasswordChangeForm)

user_model = get_user_model()


@checks.register('authpolicy')
def check_middleware(app_configs, **kwargs):
    errors = []
    middle = 'django_auth_policy.middleware.AuthenticationPolicyMiddleware'
    d_middle = 'django.contrib.auth.middleware.AuthenticationMiddleware'
    m_classes = tuple(settings.MIDDLEWARE_CLASSES)

    if not middle in m_classes:
        errors.append(checks.Critical(
                msg=('AuthenticationPolicyMiddleware is missing'),
                hint=('Add {} to MIDDLEWARE_CLASSES'.format(middle)),
                id='django_auth_policy.C001',
                ))

    if not d_middle in m_classes:
        errors.append(checks.Info(
                msg=('Djangos AuthenticationMiddleware is missing'),
                hint=('Add {} to MIDDLEWARE_CLASSES'.format(d_middle)),
                id='django_auth_policy.I003',
                ))

    if not errors and m_classes.index(d_middle) > m_classes.index(middle):
        errors.append(checks.Critical(
                msg=('Djangos AuthenticationMiddleware must come before '
                     'AuthenticationPolicyMiddleware'),
                hint=('Correct order of items in MIDDLEWARE_CLASSES'.format(d_middle)),
                id='django_auth_policy.C002',
                ))

    return errors


@checks.register('authpolicy')
def check_views(app_configs, **kwargs):
    errors = []
    # Check login view
    url = reverse('login')
    if url != settings.LOGIN_URL:
        errors.append(checks.Critical(
                msg='Login URL not equal to settings.LOGIN_URL',
                hint='Correct LOGIN_URL setting',
                id='django_auth_policy.C003',
                ))

    func, args, kwargs = resolve(url)

    if 'authentication_form' in kwargs:
        if not issubclass(kwargs['authentication_form'],
                          StrictAuthenticationForm):
            errors.append(checks.Warning(
                    msg='Login view doesn\'t use the StrictAuthenticationForm',
                    hint=None,
                    id='djang_auth_policy.W002'
                    ))
    else:
        errors.append(checks.Info(
                msg='Could not check if login view uses the StrictAuthenticationForm',
                hint=None,
                id='django_auth_policy.I001'
                ))

    # Check password change view
    url = reverse(getattr(settings, 'ENFORCED_PASSWORD_CHANGE_VIEW_NAME',
                          'password_change'))
    func, args, kwargs = resolve(url)
    if 'password_change_form' in kwargs:
        if not issubclass(kwargs['password_change_form'],
                          StrictPasswordChangeForm):
            errors.append(checks.Warning(
                    msg='password_change view doesn\'t use the StrictPasswordChangeForm',
                    hint=None,
                    id='django_auth_policy.W003'
                    ))
    else:
        errors.append(checks.Info(
                msg='Could not check if password_change view uses the StrictAuthenticationForm',
                hint=None,
                id='django_auth_policy.I002'
                ))

    return errors


@checks.register(checks.Tags.admin)
def check_admin(app_configs, **kwargs):
    errors = []
    if not 'django.contrib.admin' in settings.INSTALLED_APPS:
        return errors

    # Check login view
    if admin.site.login != admin_login:
        errors.append(checks.Warning(
                msg='admin doesn\'t use the django_auth_policy admin_login view',
                hint=None,
                id='django_auth_policy.W004'
                ))

    if not issubclass(admin.site.login_form, StrictAuthenticationForm):
        errors.append(checks.Warning(
                msg='admin doesn\'t use the django_auth_policy StrictAuthenticationForm',
                hint=None,
                id='django_auth_policy.W005'
                ))

    # Check password change
    if not admin.site.password_change == admin_password_change:
        errors.append(checks.Warning(
                msg='admin doesn\'t use the django_auth_policy admin_password_change view',
                hint=None,
                id='django_auth_policy.W006'
                ))

    # Check UserAdmin
    if not getattr(settings, 'REPLACE_AUTH_USER_ADMIN', True):
        # Replacing disabled
        pass
    elif not user_model in admin.site._registry:
        errors.append(checks.Warning(
                msg='Could not check if user admin doesn\'t use '
                    'django_auth_policy\'s StrictUserAdmin',
                hint=None,
                id='django_auth_policy.W007'
                ))
    elif not isinstance(admin.site._registry[user_model], StrictUserAdmin):
        errors.append(checks.Warning(
                msg='User admin doesn\'t use django_auth_policy\'s StrictUserAdmin',
                hint=None,
                id='django_auth_policy.W008'
                ))

    return errors
