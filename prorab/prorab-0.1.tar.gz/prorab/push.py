from boto import sqs
from boto.sqs.message import Message

from prorab import config

conn = sqs.connect_to_region(
    config.region,
    aws_access_key_id=config.id,
    aws_secret_access_key=config.key,
)


def personal(queue, message, args=''):
    q = conn.get_queue(config.queue_prefix + queue)

    m = Message()
    m.set_body(message)
    q.write(m)


def general(message):
    q = conn.get_queue(config.general_queue)

    m = Message()
    m.set_body(message)
    q.write(m)
