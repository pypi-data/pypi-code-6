from .resource import Resource
from .ref import Ref
from .event import Event
from .relation import Relation
from .page import Page


class Key(Resource):

    """
    From the Orchestrate docs:

    "Key/Value is core to Orchestrate.io. 
    All other query types are built around this data type. 
    Key/Value pairs are pieces of data
    identified by a unique key for a collection
    and have corresponding value."

    The key object represents a single key/value in Orchestrate,
    and provides methods for working with refs, events, and relations,
    as well as creating, reading, updating, and destroying key/values.

    ```python
    key = collection.key(NAME)
    # create
    response = key.put({"hello": "world"}).result()
    response.raise_for_status()
    # create a ref to work with this version of the key/value
    ref_value = response.path['ref']
    ref = key.ref(ref_value)
    # read
    response = key.get().result()
    print response.json()
    # {"hello": "world"}
    # update
    response = key.put({"goodnight": "moon"}, **{"If-Match": ref_value}).result()
    response.raise_for_status()
    ref_value = response.path['ref']
    # delete
    response = key.delete(**{"If-Match": ref_value}).result()
    response.raise_for_status()
    ```
    """

    def ref(self, name, **kwargs):
        """
        Returns an object for dealing with a given Ref value.
        See `Ref` for more info.
        """
        return self._init_child(Ref, 'refs', name, **kwargs)

    def refs(self, **kwargs):
        """
        Returns a cursor for iterating over all versions of the Key.
        """
        return self._init_child(Page, 'refs', **kwargs)

    def event(self, event_type, **kwargs):
        """
        Returns an object for creating and querying events.
        See `Event` for more info.
        """
        return self._init_child(Event, 'events', event_type, **kwargs)

    def relation(self, **kwargs):
        """
        Returns an object for creating and querying relations.
        See `Relation` for more info.
        """
        return self._init_child(Relation, **kwargs)

    def graph(self, **kwargs):
        """
        Alias to `relation`
        """
        return self.relation(**kwargs)
