from django.conf import settings
from keen import KeenClient


class KeenBlockingClient(KeenClient):

    def __init__(self):
        super(KeenBlockingClient, self).__init__(
            project_id=settings.KEEN_PROJECT_ID,
            write_key=settings.KEEN_WRITE_KEY,
            read_key=settings.KEEN_READ_KEY,
        )


class KeenCeleryClient(KeenBlockingClient):

    def add_event(self, event_collection, event_body, timestamp=None):
        from .tasks import add_event_delayed
        add_event_delayed.delay(KeenBlockingClient(), event_collection, event_body, timestamp)

    def add_events(self, events):
        from .tasks import add_events_delayed
        add_events_delayed.delay(KeenBlockingClient(), events)


def get_client():
    return KeenCeleryClient() if settings.KEEN_CELERY else KeenBlockingClient()


def add_event(event_collection, event_body, timestamp=None):
    client = get_client()
    client.add_event(event_collection, event_body, timestamp)


def add_events(events):
    client = get_client()
    client.add_events(events)