from django_messages.models import Message
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
def avisa_admin(msg, user=None):
    try:
        admin = User.objects.get(username=settings.MANAGERS)
        Message(
            subject="AVISO del sistema",
            body=msg,
            recipient=admin,
            sender=user if user != None else admin,
            ).save()
        return True
    except Exception, ex:
        return False


def week_day(day_num):
    semana = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
    return semana[day_num]
