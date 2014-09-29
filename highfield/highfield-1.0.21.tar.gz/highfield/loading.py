from highfield import naming

import pkgutil
import os

def path(folder_name):
    return os.path.join(os.getcwd(), folder_name)

def namespace(module_name):
    module_path = path(module_name)
    temp = __import__(module_name, globals(), locals(), [], -1)
    ns = type('Namespace', (object,), {})
    for name, component in generate_component(module_name, module_path):
        setattr(component, 'namespace', ns)
        setattr(ns, name, component)
        pass
    return ns

def generate_component(module_name, module_path):
    component_type_name = naming.singular(module_name)
    for loader, submodule_name in generate_submodule_loader(module_path):
        if not submodule_name.endswith(component_type_name):
            continue
            pass

        sm = submodule(loader, module_name, submodule_name)
        expected_name = naming.file_to_class(submodule_name)
        if expected_name in sm.__dict__:
            yield (naming.file_to_canonical(submodule_name),
                   sm.__dict__[expected_name])
        pass
    pass

def submodule(loader, module_name, submodule_name):
    full_module_name = '%s.%s' % (module_name, submodule_name)
    return loader.find_module(submodule_name).load_module(full_module_name)

def generate_submodule_loader(module_path):
    for loader, submodule_name, tmp in pkgutil.iter_modules([module_path]):
        yield (loader, submodule_name)
        pass
    pass
