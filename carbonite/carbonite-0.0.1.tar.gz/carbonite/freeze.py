import os
import imp
import sys
from collections import defaultdict

import pip
import pkg_resources

def get_module(relative_path):
    module_path = os.path.realpath(relative_path)
    module_name = os.path.basename(module_path).replace('.py', '')
    imp.load_source(module_name, module_path)
    return sys.modules[module_name]

def pip_install(package):
    return_code = pip.main(['install', package.replace(' ', '')])
    if return_code != 0:
        raise ValueError('installing {} failed with return code {}'.format(package, return_code))
    # prevent duplicated output, see https://github.com/pypa/pip/issues/1618
    pip.logger.consumers = []

def main():
    module = get_module(sys.argv[1])
    output_path = os.path.realpath(sys.argv[2])
    package_list_vars = module.__carbonite__

    # install all specified packages
    for var_name in package_list_vars:
        package_list = getattr(module, var_name)
        if not isinstance(package_list, list):
            raise TypeError('{}.{} must be a list of package specifications'.format(module.__name__, var_name))
        for package in package_list:
            pip_install(package)

    # construct the frozen requirements
    frozen = defaultdict(list)
    for var_name in package_list_vars:
        package_list = getattr(module, var_name)
        for package in package_list:
            package_name = pkg_resources.Requirement.parse(package).project_name
            package_version = pkg_resources.require(package_name)[0].version
            frozen[var_name].append('{}=={}'.format(package_name, package_version))

    # write the freeze file
    with open(output_path, 'w') as f:
        for var_name in package_list_vars:
            f.write('{} = [\n'.format(var_name))
            for package in frozen[var_name]:
                f.write('    "{}",\n'.format(package))
            f.write(']')
            f.write('\n\n')

    print 'Successfully froze requirements to {}'.format(output_path)

if __name__ == '__main__':
    main()
