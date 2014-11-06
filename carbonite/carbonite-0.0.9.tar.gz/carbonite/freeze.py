import os
import imp
import sys
import argparse
from collections import defaultdict

import pip
import pkg_resources

def get_module(relative_path):
    module_path = os.path.realpath(relative_path)
    module_name = os.path.basename(module_path).replace('.py', '')
    imp.load_source(module_name, module_path)
    return sys.modules[module_name]

def pip_install(package):
    return_code = pip.main(['install', '--upgrade', '--process-dependency-links', package.replace(' ', '')])
    if return_code != 0:
        raise ValueError('installing {} failed with return code {}'.format(package, return_code))
    # prevent duplicated output, see https://github.com/pypa/pip/issues/1618
    pip.logger.consumers = []

def main():
    parser = argparse.ArgumentParser(description='Freeze Python package dependencies')
    parser.add_argument('source', help='path to source file with dynamic dependencies and a __carbonite__ variable')
    parser.add_argument('dest', help='path to a new Python file that will be written with frozen dependencies')
    args = parser.parse_args()

    module = get_module(args.source)
    output_path = os.path.realpath(args.dest)
    package_list_vars = module.__carbonite__

    # install all specified packages
    for var_name in package_list_vars:
        package_list = getattr(module, var_name)
        if not isinstance(package_list, list):
            raise TypeError('{}.{} must be a list of package specifications'.format(module.__name__, var_name))
        for package in package_list:
            pip_install(package)

    reload(pkg_resources)

    # construct the frozen requirements
    frozen = defaultdict(list)
    for var_name in package_list_vars:
        package_list = getattr(module, var_name)
        for package in package_list:
            package_name = pkg_resources.Requirement.parse(package).project_name
            for subpackage in pkg_resources.require(package_name):
                spec = '{}=={}'.format(subpackage.project_name, subpackage.version)
                if spec not in frozen[var_name]:
                    frozen[var_name].append(spec)

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
