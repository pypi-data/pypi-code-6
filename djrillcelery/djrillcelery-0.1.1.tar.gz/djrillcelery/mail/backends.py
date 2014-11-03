from djrill.mail.backends.djrill import DjrillBackend
from ..tasks import send_mail


class DjrillCeleryBackend(DjrillBackend):

    def _send(self, message):
        send_mail.delay(self, message)
        return True