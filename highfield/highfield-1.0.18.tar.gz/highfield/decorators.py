from highfield.helpers.random import unique_id
from highfield.errors import *

from datetime import datetime as dt

import time

def original(decorator, *args, **kwargs):
    def wrapper(*args, **kwargs):
        wrapped = decorator(*args, **kwargs)
        if hasattr(args[0], 'original'):
            wrapped.original = args[0].original
            pass
        else:
            wrapped.original = args[0]
            pass
        return wrapped
    return wrapper

@original
def datetime(func):
    def wrapper(*args, **kwargs):
        kwargs.update(datetime=dt.utcnow())
        return func(*args, **kwargs)
    return wrapper

@original
def timestamp(func):
    def wrapper(*args, **kwargs):
        utc_timestamp = int(time.mktime(dt.utcnow().timetuple()))
        kwargs.update(timestamp=utc_timestamp)
        return func(*args, **kwargs)
    return wrapper

@original
def validator(func):
    def wrapper(*args, **kwargs):
        controller = args[0]
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            controller.context.setdefault('validation_errors', {})
            controller.context['validation_errors'].update(e.errors)
            return controller.render()
        pass
    return wrapper

@original
def csrf(func):
    def wrapper(*args, **kwargs):
        controller = args[0]
        utc_timestamp = kwargs.get('timestamp')
        if not utc_timestamp:
            utc_timestamp = int(time.mktime(dt.utcnow().timetuple()))
            pass

        csrf_token = controller.session.get('csrf_token')
        csrf_expires = int(controller.session.get('csrf_expires', 0))
        csrf_token_expired = False
        if not (csrf_token and csrf_expires) or csrf_expires < utc_timestamp:
            if csrf_token:
                csrf_token_expired = True
                pass
            controller.session.update(csrf_token=unique_id(24),
                                      csrf_expires=utc_timestamp + controller.app.csrf_token_lifespan)
            pass
        if controller.post:
            if controller.form.get('csrf_token') != csrf_token:
                if csrf_token_expired:
                    string = 'The form timed out before submission as a security measure. Please try again.'
                    pass
                else:
                    string = 'The form submission token did not match the session. Submision was stopped as a security measure.'
                    pass
                raise ValidationError({controller.model.canonical_name: string})
                pass
            pass

        controller.context.update(csrf_token=controller.session['csrf_token'])
        return func(*args, **kwargs)
    return wrapper

