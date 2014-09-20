import uuid

def unique_id(length):
    return str(uuid.uuid4().get_hex().upper()[:length])
