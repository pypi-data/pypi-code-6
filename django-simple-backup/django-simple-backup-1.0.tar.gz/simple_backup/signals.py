import django.dispatch

backup_ready = django.dispatch.Signal(providing_args=['path',])
