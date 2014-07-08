class BaseSubscriber(object):
    """
    The listener method of this object will run in its own thread
    in an infinite loop.
    """

    # Something to produce data consumed by the listner
    data_producer = None

    def listener(self, web_socket_instance):
        raise NotImplementedError
