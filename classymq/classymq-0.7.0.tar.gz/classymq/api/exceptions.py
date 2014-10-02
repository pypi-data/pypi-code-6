__author__ = 'gdoermann'

class DeadMethodException(Exception):
    """
    This should be thrown in a method that is handled by an amqp api.
    The api should remove the message when raised..
    """