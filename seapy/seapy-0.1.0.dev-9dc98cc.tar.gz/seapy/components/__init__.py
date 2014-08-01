"""
Components
==========

.. toctree::
    :maxdepth: 2


Module with all components that are available.

.. inheritance-diagram:: seapy.components

.. automodule:: seapy.components.component

Structural
**********

.. automodule:: seapy.components.componentstructural
.. automodule:: seapy.components.component1dbeam
.. automodule:: seapy.components.component1dpipe
.. automodule:: seapy.components.component2dplate


Acoustical
**********

.. automodule:: seapy.components.componentacoustical
.. automodule:: seapy.components.component1dcavity
.. automodule:: seapy.components.component2dcavity
.. automodule:: seapy.components.component3dcavity


"""

from .component1dbeam import Component1DBeam
from .component2dplate import Component2DPlate

from .component2dacoustical import Component2DAcoustical
from .component3dacoustical import Component3DAcoustical


import inspect, sys
components_map = {item[0]: item[1] for item in inspect.getmembers(sys.modules[__name__], inspect.isclass)}
"""
Dictionary with all available components.
""" 
