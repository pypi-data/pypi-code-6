"""
The ID constants for all known simulation models.

Example::

    from vecnet.simulation import sim_model

    def my_function(model, ...):
        if model == sim_model.OPEN_MALARIA:
            # do something special for OpenMalaria
            ...
        else:
            # handle all other simulation models in the same way
            ...
"""

# Short strings are used to facilitate debugging
EMOD         = 'EMOD'  #: EMOD
OPEN_MALARIA = 'OM'    #: OpenMalaria http://code.google.com/p/openmalaria/wiki/Start
MOCK         = 'mock'  #: fake model for testing purposes

ALL = (
    EMOD,
    OPEN_MALARIA,
    MOCK,
)  #: List of all known IDs.

MAX_LENGTH = 4  #: For use when storing IDs in a database field, e.g. CharField(max_length=sim_model.MAX_LENGTH)


def is_valid(model_id):
    """
    Is an model ID a known value?

    :param str model_id: The model ID to check
    :returns: True or False
    """
    return model_id in ALL


_names = {
    EMOD:         "EMOD",
    MOCK:         "mock",
    OPEN_MALARIA: "OpenMalaria",
}


def get_name(model_id):
    """
    Get the name for a model.

    :returns str: The model's name.  If the id has no associated name, then "id = {ID} (no name)" is returned.
    """
    name = _names.get(model_id)
    if name is None:
        name = 'id = %s (no name)' % str(model_id)
    return name