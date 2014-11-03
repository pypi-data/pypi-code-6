from celery.task import task

@task
def send_mail(obj, message):
    from .mail.backends import DjrillCeleryBackend
    super(DjrillCeleryBackend, obj)._send(message)