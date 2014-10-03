import protopigeon


def serialize(MessageType, entity):
    return protopigeon.to_message(entity, MessageType)


def deserialize(Model, message):
    return protopigeon.to_entity(message, Model)


def serialize_list(ListMessageType, entities):
    from .ndb import PaginationResults
    from .search import SearchResults

    if isinstance(entities, (PaginationResults, SearchResults)):
        next_page_token = entities.next_page_token
        entities = entities.items
    else:
        next_page_token = None

    MessageType = ListMessageType.items.message_type

    message = ListMessageType()
    message.items = [serialize(MessageType, x) for x in entities]
    message.next_page_token = next_page_token

    return message
