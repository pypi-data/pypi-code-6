from . import data_types

class Recursion:

    def __init__(self, client):
        self.__client = client

    def create(self, *args, **kwargs):
        """        Create a recursion object with given parameters.

        Args:
            - RecursionRequestCreate
            - Value convertible to RecursionRequestCreate
            - kwargs corresponds to RecursionRequestCreate

        Returns:
            the API response in RecursionResponse
        """
        req = data_types.RecursionRequestCreate.create(kwargs if len(args) == 0 else args[0])
        raw_response = self.__client.request('post', 'recursions', req.to_raw_params())
        return data_types.RecursionResponse(raw_response)

    def retrieve(self, *args, **kwargs):
        """        Retrieve a recursion object by recursion id.
        If the recursion is already deleted, "deleted" attribute becomes true.

        Args:
            - RecursionIdRequest
            - Value convertible to RecursionIdRequest
            - kwargs corresponds to RecursionIdRequest

        Returns:
            the API response in RecursionResponse
        """
        req = data_types.RecursionIdRequest.create(kwargs if len(args) == 0 else args[0])
        raw_response = self.__client.request('get', 'recursions' + '/' + str(req.id), req.to_raw_params())
        return data_types.RecursionResponse(raw_response)

    def resume(self, *args, **kwargs):
        """        Resume a suspended recursion

        Args:
            - RecursionRequestResume
            - Value convertible to RecursionRequestResume
            - kwargs corresponds to RecursionRequestResume

        Returns:
            the API response in RecursionResponse
        """
        req = data_types.RecursionRequestResume.create(kwargs if len(args) == 0 else args[0])
        raw_response = self.__client.request('post', 'recursions' + '/' + str(req.id) + '/' + 'resume', req.to_raw_params())
        return data_types.RecursionResponse(raw_response)

    def delete(self, *args, **kwargs):
        """        Delete an existing recursion

        Args:
            - RecursionIdRequest
            - Value convertible to RecursionIdRequest
            - kwargs corresponds to RecursionIdRequest

        Returns:
            the API response in RecursionResponse
        """
        req = data_types.RecursionIdRequest.create(kwargs if len(args) == 0 else args[0])
        raw_response = self.__client.request('delete', 'recursions' + '/' + str(req.id), req.to_raw_params())
        return data_types.RecursionResponse(raw_response)

    def all(self, *args, **kwargs):
        """        List recursions filtered by params

        Args:
            - ListRequestWithCustomerAndSuspended
            - Value convertible to ListRequestWithCustomerAndSuspended
            - kwargs corresponds to ListRequestWithCustomerAndSuspended

        Returns:
            the API response in RecursionResponseList
        """
        req = data_types.ListRequestWithCustomerAndSuspended.create(kwargs if len(args) == 0 else args[0])
        raw_response = self.__client.request('get', 'recursions', req.to_raw_params())
        return data_types.RecursionResponseList(raw_response)

