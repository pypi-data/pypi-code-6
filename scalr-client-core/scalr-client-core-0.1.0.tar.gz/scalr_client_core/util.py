# coding:utf-8

def unpack_sets(obj):
    """
    Unpack all ObjectSet[Item] entries into the actual lists, removing the
    Item entry entirely.
    """
    if isinstance(obj, dict):
        for key, value in list(obj.items()):  # Forward compatibility with Python 3
            if key.endswith("Set"):
                if value is None:                       # This means no Items!
                    items = []
                elif isinstance(value, dict):
                    if value.keys() == ["Item"]:        # This means one or multiple Items!
                        items = value["Item"]
                        if isinstance(items, dict):     # If we only have one Item, wrap it in a list
                            items = [items]
                    else:
                        assert False, "This should never happen"
                else:
                    assert False, "This should never happen"
                obj[key] = items
        map(unpack_sets, obj.values())
    elif isinstance(obj, (list, tuple, set)):
        map(unpack_sets, obj)
    else:
        pass