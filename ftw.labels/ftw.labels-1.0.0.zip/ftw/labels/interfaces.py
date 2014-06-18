from zope.interface import Interface


class ILabelRoot(Interface):
    """Marker interface for label roots, which have their own ecosystem
    of labels.
    """


class ILabelSupport(Interface):
    """Marker interface for objects which support labelling.
    All objects providing this interface must be within a container
    providing ``ILabelRoot``.
    """


class ILabelJar(Interface):
    """Adapter interface for label roots (``ILabelRoot``), providing
    an interface for managing available labels for this label ecosystem.
    """

    def __init__(context):
        """Adapts a label root.
        """

    def add(title, color):
        """Adds a new label with ``title`` and ``color``.
        Returns the id of the new label as string.
        """

    def remove(label_id):
        """Removes the label with ID ``label_id``.
        If the label was successfully removed, ``True`` is returned.
        If there is no such label, ``False`` is returned.
        """

    def update(label_id, title, color):
        """Updates the label with ID ``label_id``.
        Raises a ``KeyError`` when there is no such label.
        """

    def get(label_id):
        """Returns a dict with the label information for the label
        with ID ``label_id``.

        Example:

        {'label_id': 'label-id',
         'title': 'Label Title',
         'color': '#FF0000'}
        """

    def list():
        """Returns all available labels as list of dicts.

        Example:
        [
            {'label_id': 'label-id',
             'title': 'Label Title',
             'color': '#FF0000'},

            {'label_id': 'another-label-id',
             'title': 'Another Label Title',
             'color': '#0000FF'},
        ]
        """


class ILabeling(Interface):
    """Adapter interface for objects which provide ``ILabelSupport``,
    providing an interface for setting, updating and removing the
    labels of this object.
    """

    def __init__(context):
        """Adapts any object with ``ILabelSupport``.
        """

    def update(label_ids):
        """Set the active labels for the current context by passing in a list
        of label IDs.
        Labels which where activated before but are not in the ``label_ids``
        are purged.
        """

    def active_labels():
        """Returns all active labels on the current object as list of dicts.

        Example:
        [
            {'label_id': 'label-id',
             'title': 'Label Title',
             'color': '#FF0000'},

            {'label_id': 'another-label-id',
             'title': 'Another Label Title',
             'color': '#0000FF'},
        ]
        """

    def available_labels():
        """Returns all labels available in the current ecosystem, each as
        dict, with additional information whether it is activated on the
        current object or not.

        Example:
        [
            {'label_id': 'label-id',
             'title': 'Label Title',
             'color': '#FF0000',
             'active': True},

            {'label_id': 'another-label-id',
             'title': 'Another Label Title',
             'color': '#0000FF',
             'active': False},
        ]
        """
