from celery import Celery
from datetime import timedelta


app = Celery(
    'swisschard',
    broker='redis://',
    backend='redis://',
    include=[
        'tests.test_integration',
    ]
)

app.conf.update(
    CELERYD_CONCURRENCY=1,
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER="json",
    CELERY_TASK_RESULT_EXPIRES=timedelta(hours=1),
    CELERYBEAT_SCHEDULER="swisschard.scheduler.ChardScheduler",
    CELERY_REDIS_SCHEDULER_URL="redis://",
    CELERYBEAT_SCHEDULE = {
        'heart_beat': {
            'task': 'tests.test_integration.EchoTask',
            'schedule': timedelta(seconds=1)
        },
    }
)

