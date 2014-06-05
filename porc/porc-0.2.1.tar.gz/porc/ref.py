from .resource import Resource


class Ref(Resource):

    """
    From the Orchestrate docs:

    "Refs are used to identify specific immutable values that have been assigned to keys."

    Ref objects allow you to work with specific versions of a doc,
    particularly past versions.

    ```python
    ref = key.ref(ref_value)
    response = ref.get().result()
    print response.json()
    # {"hello": "world"}
    ```
    """
    # everything is defined by the parent :D
    pass
