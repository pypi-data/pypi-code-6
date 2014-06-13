from urlparse import urlparse
import glob
import os
import imp



def get_protocol(url):
    parsed_url = urlparse(url)
    return parsed_url.scheme


def get_hostname(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc


def is_path(url):
    """ Determine if the given url is just a path """

    parsed_url = urlparse(url)

    if parsed_url[0] == '' or parsed_url[1] == '':
        return True
    else:
        return False


def get_percentage(partial, total):
    return float(partial) / float(total)


def get_all_modules_from_dir(directory):
    """
    Given a directory, load all of the modules (Classes) within it.
    """

    glob_path = os.path.join(directory, '[a-zA-Z]*.py')
    file_list = glob.glob( glob_path )

    plugin_list = []
    for filename in file_list:
        module = load_module_from_file(filename)
        plugin_list.append(module)

    return plugin_list


def load_module_from_file(filepath):
    """
    Given a filename, return the class with the same name.
    """

    mod_name, file_ext = get_filename_info(filepath)

    if file_ext.lower() == '.py':
        py_mod = imp.load_source(mod_name, filepath)

    # elif file_ext.lower() == '.pyc':
    #     py_mod = imp.load_compiled(mod_name, filepath)

    klass = getattr(py_mod, mod_name)

    return klass


def get_filename_info(filepath):
    """
    Gets the name of a file and its extention
    """

    filename = os.path.split(filepath)[-1]
    mod_name, file_ext = os.path.splitext(filename)

    return mod_name, file_ext


def get_best_path(path):
    """
    Determine if `path` exists, otherwise create it.
    If None is passed, return current working directory.
    """

    new_path = path

    if new_path is None:
        new_path = os.getcwd()

    else:
        new_path = os.path.expanduser(new_path)

        if not os.path.isdir(new_path):
            new_path = os.makedirs(new_path)

    return new_path
