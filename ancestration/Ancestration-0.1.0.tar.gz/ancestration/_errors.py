from __future__ import unicode_literals

from ancestration import FamilyInheritanceError

invalid_adoption_object = lambda obj: FamilyInheritanceError(
    'Invalid object to adopt into family, only classes and functions are allowed: {}'.format(obj))
multiple_family_declarations = lambda: FamilyInheritanceError(
    'A module may be made a family module only once.')
invalid_family_extends = lambda extends: FamilyInheritanceError(
    'Only family modules can be family-extented, but is {}.'.format(type(extends)))
outside_family = lambda: FamilyInheritanceError(
    'A family class may only be defined in a family module.')
multiple_family_bases = lambda: FamilyInheritanceError(
    'A family class may not extend more than one family class.')
different_family_base = lambda: FamilyInheritanceError(
    'The redefined family class has a different family base class than the original.')
no_super_family = lambda: FamilyInheritanceError(
    '"FAMILY_INHERIT" was given but there is no super family.')
no_super_family_base = lambda cls_name: FamilyInheritanceError(
    '"FAMILY_INHERIT" contains "{}", but no equally named class was found in the super family.'.format(cls_name))
missing_attribute = lambda attr_name: FamilyInheritanceError(
    'The "FAMILY_INHERIT" attribute "{}" does not exist in super family base.'.format(attr_name))
def adoption_import_error(family_module, module, import_error):
    error_module = import_error.__class__.__module__
    if error_module is None or error_module == '__builtin__':
        error_module = ''
    error_qualified_name = error_module + '.' + import_error.__class__.__name__
    message = 'Could not adopt the module "{}" into family "{}", because an exception of type "{}" was raised'.format(
            module, family_module.__name__, error_qualified_name)
    error_message = '{}'.format(import_error)
    if len(error_message) == 0:
        message += '.'
    else:
        message += ' with message: {}'.format(error_message)
    return FamilyInheritanceError(message)