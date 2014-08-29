import sys
from pyramid_sqlalchemy import init_sqlalchemy
from pyramid_sqlalchemy import model

# BBB Alias
sys.modules['s4u.sqlalchemy.model'] = model

def includeme(config):
    """'Convenience method to initialise all components of this
    :mod:`s4u.sqlalchemy` package from a pyramid applicaiton.
    """
    config.include('pyramid_sqlalchemy')
