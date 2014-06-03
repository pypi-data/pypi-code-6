from . import data_types

class Event:

    def __init__(self, client):
        self.__client = client

    def retrieve(self, *args, **kwargs):
        """        Retrieve an event object by event id.

        Args:
            - EventIdRequest
            - Value convertible to EventIdRequest
            - kwargs corresponds to EventIdRequest

        Returns:
            the API response in EventResponse
        """
        req = data_types.EventIdRequest.create(kwargs if len(args) == 0 else args[0])
        raw_response = self.__client.request('get', 'events' + '/' + str(req.id), req.to_raw_params())
        return data_types.EventResponse(raw_response)

    def all(self, *args, **kwargs):
        """        List events filtered by params

        Args:
            - ListRequestWithEventType
            - Value convertible to ListRequestWithEventType
            - kwargs corresponds to ListRequestWithEventType

        Returns:
            the API response in EventResponseList
        """
        req = data_types.ListRequestWithEventType.create(kwargs if len(args) == 0 else args[0])
        raw_response = self.__client.request('get', 'events', req.to_raw_params())
        return data_types.EventResponseList(raw_response)

