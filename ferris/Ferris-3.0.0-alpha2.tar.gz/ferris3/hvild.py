import ferris3

#
# Method implementations.
# Bare-bones, can be re-used in other methods and such.
#


def list_impl(ListMessage, query):
    return ferris3.ToolChain(query) \
        .messages.serialize_list(ListMessage) \
        .value()


def paginated_list_impl(ListMessage, query, limit, page_token):
    return ferris3.ToolChain(query) \
        .ndb.paginate(limit=limit, page_token=page_token) \
        .messages.serialize_list(ListMessage) \
        .value()


def searchable_list_impl(ListMessage, index, query, limit, sort, page_token):
    def check_for_search_errors(data):
        if data.error:
            raise ferris3.BadRequestException("Search error: %s" % data.error)

    return ferris3.ToolChain(query) \
        .search.search(index, sort=sort, limit=limit, page_token=page_token) \
        .tap(check_for_search_errors) \
        .search.to_entities() \
        .messages.serialize_list(ListMessage) \
        .value()


def get_impl(Model, Message, item_key):
    return ferris3.ToolChain(item_key) \
        .ndb.get() \
        .raise_if(None, ferris3.NotFoundException()) \
        .ndb.check_kind(Model) \
        .messages.serialize(Message) \
        .value()


def delete_impl(Model, item_key):
    return ferris3.ToolChain(item_key) \
        .ndb.key() \
        .ndb.check_kind(Model) \
        .ndb.delete() \
        .value()


def update_impl(Model, Message, item_key, request):
    item = ferris3.ToolChain(item_key) \
        .ndb.get() \
        .raise_if(None, ferris3.NotFoundException()) \
        .ndb.check_kind(Model) \
        .value()

    return ferris3.ToolChain(request) \
        .messages.deserialize(item) \
        .ndb.put() \
        .messages.serialize(Message) \
        .value()


def insert_impl(Model, Message, request):
    return ferris3.ToolChain(request) \
        .messages.deserialize(Model) \
        .ndb.put() \
        .messages.serialize(Message) \
        .value()

#
# Full method wrappers.
# Can be used as endpoint methods directly.
#


def list(Model, Message=None, ListMessage=None, query=None, name='list'):
    if not Message:
        Message = ferris3.model_message(Model)

    if not ListMessage:
        ListMessage = ferris3.list_message(Message)

    if not query:
        query = Model.query()

    if callable(query):
        query = query()

    @ferris3.auto_method(returns=ListMessage, name=name)
    def inner(self, request):
        return list_impl(ListMessage, query)

    return inner


def paginated_list(Model, Message=None, ListMessage=None, query=None, limit=50, name='paginated_list'):
    if not Message:
        Message = ferris3.model_message(Model)

    if not ListMessage:
        ListMessage = ferris3.list_message(Message)

    if not query:
        query = Model.query()

    if callable(query):
        query = query()

    @ferris3.auto_method(returns=ListMessage, name=name)
    def inner(self, request, page_token=(str, '')):
        return paginated_list_impl(ListMessage, query, limit, page_token)

    return inner


def searchable_list(Model=None, Message=None, ListMessage=None, limit=50, index=None, name='search'):
    if not Message:
        Message = ferris3.model_message(Model)

    if not ListMessage:
        ListMessage = ferris3.list_message(Message)

    if not index:
        index = ferris3.search.index_for(Model)

    @ferris3.auto_method(returns=ListMessage, name=name)
    def inner(self, request, query=(str, ''), sort=(str, None), page_token=(str, '')):
        return searchable_list_impl(ListMessage, index, query, limit, sort, page_token)

    return inner


def get(Model, Message=None, name='get'):
    if not Message:
        Message = ferris3.model_message(Model)

    @ferris3.auto_method(returns=Message, name=name)
    def inner(self, request, item_key=(str,)):
        return get_impl(Model, Message, item_key)

    return inner


def delete(Model, name='delete'):

    @ferris3.auto_method(name=name, http_method='DELETE')
    def inner(self, request, item_key=(str,)):
        delete_impl(Model, item_key)
        return None

    return inner


def insert(Model, Message=None, name='insert'):
    if not Message:
        Message = ferris3.model_message(Model)

    @ferris3.auto_method(returns=Message, name=name, http_method='POST')
    def inner(self, request=(Message,)):
        return insert_impl(Model, Message, request)

    return inner


def update(Model, Message=None, name='update'):
    if not Message:
        Message = ferris3.model_message(Model)

    @ferris3.auto_method(returns=Message, name=name, http_method='POST')
    def inner(self, request=(Message,), item_key=(str,)):
        return update_impl(Model, Message, item_key, request)

    return inner
