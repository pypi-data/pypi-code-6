"""
dynamictop
==========

A toolset for creating dynamic top information for salt.

This can create dynamic top information for both states and pillars

.. note::
    For now this tool assumes you're matching the dynamic top information using
    grains
"""
import os
import yaml


def process_dynamic_top(dynamic_path, grain_value):
    """Process a path for a single dynamic top directory

    If used standalone, this function is intended for use with master_tops

    :param dynamic_path: The path to find the generated directories
    :type dynamic_path: str
    :param grain_value: The value of the grain that is being used to select the
                        dynamic top path
    :type grain_value: str
    :returns: list -- A list of new states to include for this dynamic_top
    """
    dynamic_top_sls_path = os.path.join(dynamic_path, grain_value, 'top.sls')
    if not os.path.exists(dynamic_top_sls_path):
        return []
    dynamic_top = yaml.load(open(dynamic_top_sls_path).read())

    include_states = map(lambda state: "%s.%s" % (grain_value, state),
                         dynamic_top['base']['*'])
    return include_states


def process_dynamic_tops(dynamic_path, grain_template):
    """Processes a path full of generated directories to gather the dynamic top
    information

    This function is intended for use with a #!py salt renderer

    :param dynamic_path: The path to find the generated directories
    :type dynamic_path: str
    :param grain_template: A sprintf style string that is used to generate the
                           salt grain matcher
    :type grain_template: str

    :returns: dict -- The dictionary of dynamic top information. This should
                      likely go into the base['*'] section of the top.sls

    """
    dynamic_tops = {}

    for dir_name in os.listdir(dynamic_path):
        matcher = grain_template % dir_name

        dynamic_includes = [{'match': 'grain'}]

        dynamic_includes.extend(
            process_dynamic_top(dynamic_path, dir_name)
        )
        dynamic_tops[matcher] = dynamic_includes
    return dynamic_tops


def generate_top(base_top_sls_path, dynamic_path, grain_template):
    """Generate top information combining a base sls file and dynamically
    generated top information

    :param base_top_sls_path: The path to the sls file to use as a base. Assumed
                              to be an absolute path
    :type base_top_sls_path: str
    :param dynamic_path: The path to find the generated directories
    :type dynamic_path: str
    :param grain_template: A sprintf style string that is used to generate the
                           salt grain matcher
    :type grain_template: str
    """
    top = yaml.load(open(base_top_sls_path).read())
    dynamic_tops = process_dynamic_tops(dynamic_path, grain_template)
    top['base'].update(dynamic_tops)
    return top
