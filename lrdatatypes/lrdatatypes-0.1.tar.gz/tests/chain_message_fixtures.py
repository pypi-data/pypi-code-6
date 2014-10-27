from datatypes.core import unicoded

# This message has the generated database IDs etc in it
valid_chain_message = unicoded({
    'message_envelope': {
        'caused_by_blockchain_insert_id': 3954,

        'message': {
            'message': {
                'object': {
                    'reason_for_change': 'str',
                    'db_id': 3953,
                    'data': '<data>',
                    'initial_request_timestamp': '123456',
                    'created_by': 'The Mint',
                    'creation_timestamp': 1,
                    'object_id': 'AB12345',
                    'chains': [
                        {
                            'chain_name': 'history',
                            'chain_value': 'AB12345'
                        },
                        {
                            'chain_name': 'sausage',
                            'chain_value': 'walls'
                        }
                    ],
                    'blockchain_index': 3953
                },
            },
            'chain_name': 'sausage',
        },
    }
})

# This message does not have the generated database IDs in it
another_valid_message = unicoded({
    'message_envelope': {
        'caused_by_blockchain_insert_id': 4188,
        'message': {
            'message': {
                'object': {
                    'reason_for_change': 'str',
                    'data': '<data>',
                    'initial_request_timestamp': '123456',
                    'created_by': 'The Mint',
                    'object_id': 'AB12345',
                    'chains': [
                        {
                            'chain_name': 'history',
                            'chain_value': 'AB12345'
                        },
                        {
                            'chain_name': 'sausage',
                            'chain_value': 'walls'
                        }
                    ]
                }
            },
            'chain_name': 'sausage'
        }
    }
})

