from .base import BaseSubscriber


class RedisSubscriber(BaseSubscriber):

    kill_channel = "__KILL__"

    def __init__(self, client, options):
        self.redis_client = client
        channels = options.redis_channels
        if channels is None:
            channels = ["global"]
        channels += [self.kill_channel]
        self.data_producer = self.redis_client.pubsub()
        self.data_producer.subscribe(channels)
        self.__KILL__ = False

    def kill(self):
        self.__KILL__ = True
        self.redis_client.publish(self.kill_channel, "#YOLO")

    def listener(self, web_socket_instance):
        # Adds data to the web_socket_instance's queue so that
        # a consumer can act on it.
        for data in self.data_producer.listen():
            web_socket_instance.queue.put(data)
            if self.__KILL__ is True:
                self.data_producer.unsubscribe()
                break
