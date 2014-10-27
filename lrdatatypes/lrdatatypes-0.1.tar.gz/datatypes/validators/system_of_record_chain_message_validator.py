from voluptuous import Required, Coerce

from datatypes.core import DictionaryValidator
from datatypes.validators import system_of_record_request_validator


schema = {
    Required('message_envelope'): {
        Required('caused_by_blockchain_insert_id'): Coerce(int),
        Required('message'):
            {
                Required('message'): system_of_record_request_validator.schema,
                Required('chain_name'): unicode,
            }
    }
}


class SystemOfRecordChainMessageValidator(DictionaryValidator):
    def define_schema(self):
        return schema

    def define_error_dictionary(self):
        return {
            'message_envelope': 'message_envelope is a required field',
            'message_envelope.caused_by_blockchain_insert_id': 'Must be an integer',
            'message_envelope.messages': 'Must be an array of message objects with a message and chain name',
            'message_envelope.messages.message': 'Must be a valid system of record message',
            'message_envelope.messages.chain_name': 'Must be the name of the chain for this message'
        }
