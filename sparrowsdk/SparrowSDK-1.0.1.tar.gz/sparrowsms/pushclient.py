import types
import requests
from urllib import urlencode

from settings import SPARROW_OUTGOING_SMS_API_URL, UNICODE_FLAGS
from utils import url_call_post


class PushClient(object):

    def __init__(self, client_id, username, password):
        self.client_id = client_id
        self.username = username
        self.password = password
        self.url = SPARROW_OUTGOING_SMS_API_URL
        self.shortcode = None
        self.identity = None
        self.subaccount = None
        self.tag = None
        self.unicode = 'false'
        self.message_queue = []
        self.response_queue = []
        self.response_format = 'json'



    '''
    Setters for all the variables used in PushClient
    '''

    def set_from(self, shortcode):
        self.shortcode = shortcode

    def set_identity(self, identity):
        self.identity = identity

    def set_subaccount(self, subaccount):
        self.subaccount = subaccount

    def set_tag(self, tag):
        self.tag = tag

    def set_unicode_flag(self, unicode_flag=False):
        if unicode_flag in UNICODE_FLAGS['TRUE']:
            self.unicode = 'true'
        elif unicode_flag in UNICODE_FLAGS['FALSE']:
            self.unicode = 'false'
        elif unicode_flag in UNICODE_FLAGS['AUTO']:
            self.unicode = 'auto'
        else:
            raise ValueError("Only (True, 'True', 'true', '1', 1), (False, 'False', 'false', '0', 0) or ('Auto', 'auto', '2', 2) supported.")

    def set_response_format(self, response_format):
        if response_format in ('json', 'text'):
            self.response_format = response_format
        else:
            raise ValueError("Only 'json' or 'text' supported.")


    '''
    Getters for all the variables used in PushClient
    '''

    def get_from(self):
        return self.shortcode

    def get_identity(self):
        return self.identity

    def get_subaccount(self):
        return self.subaccount

    def get_tag(self):
        return self.tag

    def get_unicode_flag(self):
        if self.unicode_flag == 'true':
            return True
        elif self.unicode_flag == 'auto':
            return 'Auto'
        else:
            return False

    def get_response_format(self):
        return self.response_format



    '''
    Check the credit status of the account
    '''
    def credit_status(self):
        params = {
            "client_id":self.client_id,
            "username":self.username,
            "password":self.password,
            "intent":'credits',
        }
        response = url_call_post(self.url, values=params)
        return response



    '''
    Request Credit Top Up
    '''
    def request_topup(self, amount):
        params = {
            "client_id":self.client_id,
            "username":self.username,
            "password":self.password,
            "intent":'topup',
            "amount":amount,
        }
        response = url_call_post(self.url, values=params)
        return response



    '''
    Process destination_chunk and enqueue message and destination set to the message_queue before send request is initiated
    '''
    def enqueue(self, destination, message):
        destination_chunk = self.parse_destinations_to_chunk(destination)
        self.enqueue_parsed_message(destination_chunk, message)
        return self.message_queue

    '''
    Create destination_chunk if destination provided in tuple, list or string (phone no.s seperated by commas)
    '''
    def parse_destinations_to_chunk(self, destination):
        if isinstance(destination, (types.TupleType, types.ListType)):
            return self.create_chunk(destination)
        elif isinstance(destination, types.StringType):
            destination_list = destination.split(",")
            return self.create_chunk(destination_list)
        else:
            raise TypeError("Only Tuple, List or String supported.")

    '''
    Create the actual destination_chunk
    '''
    def create_chunk(self, destination_list):
        destination_chunk = []
        start = 0
        length = len(destination_list)
        while start<length:
            destination_chunk.append(",".join(destination_list[start:start+5]))
            start = start+5
        return destination_chunk

    '''
    Add the destination_chunk and message combo to sending message_queue
    '''
    def enqueue_parsed_message(self, destination_chunk, message):
        for chunk in destination_chunk:
            self.message_queue.append({"destination_chunk":chunk, "message":message,})

    '''
    Pop first member of the message_queue
    '''
    def pop_message_queue(self):
        if self.message_queue:
            return self.message_queue.pop(0)
        else:
            return False

    '''
    Fetch the required params and the provided optional params for send()
    '''
    def sms_params(self, message_set):
        params = {
            "client_id":self.client_id,
            "username":self.username,
            "password":self.password,
            "intent":'sms',
        }
        params["to"] = message_set["destination_chunk"]
        params["text"] = message_set["message"]
        if self.shortcode:
            params["shortcode"] = self.shortcode
        if self.identity:
            params["identity"] = self.identity
        if self.subaccount:
            params["subaccount"] = self.subaccount
        if self.tag:
            params["tag"] = self.tag
        if self.unicode:
            params["unicode"] = self.unicode
        if self.response_format:
            params["format"] = self.response_format
        return params

    '''
    Actual initiation of the sending sms from the message_queue
    Additional sms queueing and resetting the optional parameters during initiation of the send request
    '''
    def send(self, **kwargs):
        self.parse_kwargs(**kwargs)
        for message_set in self.message_queue:
            sms_params = self.sms_params(message_set)
            response = url_call_post(self.url, values=sms_params)
            message_set["response"] = response
            self.response_queue.append(message_set)
        return self.response_queue

    '''
    Parse the parameters supplied while invoking send()
    '''
    def parse_kwargs(self, **kwargs):
        if kwargs.get("destination") and kwargs.get("message"):
            self.enqueue(destination=kwargs.get("destination"), message=kwargs.get("message"))
        if kwargs.get("shortcode"):
            self.set_shortcode(kwargs.get("shortcode"))
        if kwargs.get("identity"):
            self.set_identity(kwargs.get("identity"))
        if kwargs.get("unicode_flag"):
            self.set_unicode_flag(kwargs.get("unicode_flag"))
        if kwargs.get("subaccount"):
            self.set_subaccount(kwargs.get("subaccount"))
        if kwargs.get("tag"):
            self.set_tag(kwargs.get("tag"))
        if kwargs.get("response_format"):
            self.set_response_format(kwargs.get("response_format"))

    '''
    Flush message_queue
    '''
    def flush(self):
        self.message_queue = []
        return self.message_queue

    '''
    Only simulate the sms send request
    Returns equivalent curl commands
    '''
    def simulate(self):
        curl_commands = []
        for message_set in self.message_queue:
            sms_params = self.sms_params(message_set)
            request_obj = requests.Request(method='POST', url=SPARROW_OUTGOING_SMS_API_URL, data=sms_params)
            prepared_req_obj = request_obj.prepare()
            curl_commands.append(self.curl_request(prepared_req_obj))
        return curl_commands

    '''
    Generate equivalent curl command from prepared request object
    '''
    def curl_request(self, request):
        command = "curl -X {method} -H {headers} -d {data} {uri}"
        method = request.method
        uri = request.url
        data = request.body
        headers = ["{0}: {1}".format(k, v) for k, v in request.headers.items()]
        headers = " -H ".join(headers)
        return command.format(method=method, headers=headers, data=data, uri=uri)