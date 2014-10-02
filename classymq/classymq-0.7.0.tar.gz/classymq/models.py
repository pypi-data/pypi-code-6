import logging
from classymq.event import events
from classymq.event.producer import EventProducer

__author__ = 'gdoermann'

logger = logging.getLogger(__name__)

class RabbitModelMixin(object):
    """
    Allow for django models to dynamically create their own consumers and producers.

    """
    AMQP_KEY = 'slug'

    @property
    def amqp_key(self):
        if callable(self.AMQP_KEY):
            return self.AMQP_KEY(self)
        else:
            return self.AMQP_KEY

    def amqp_producer(self):
        return

    def amqp_broadcast(self, event, fail_silently=False):
        notifier = EventProducer()
        logger.info('Sending message %s to exchange: %s, routing key: %s, delivery mode: %s' % (
            event, notifier.exchange_name, notifier.message_routing_key(event), notifier.DELIVERY_MODE))
        try:
            notifier.send_message(event)
        except Exception:
            if fail_silently:
                return
            else:
                raise

    def amqp_creation_event(self):
        return events.CreationEvent(self.__class__.__name__, self.pk)

    def amqp_activation_event(self, active=True):
        return events.ActivationEvent(self.__class__.__name__, self.pk, active)

    def amqp_update_event(self, **kwargs):
        return events.UpdateEvent(self.__class__.__name__, self.pk, **kwargs)
