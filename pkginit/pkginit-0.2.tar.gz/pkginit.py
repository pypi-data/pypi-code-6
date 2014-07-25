def load_modules(file_path):
    from os import path
    pkg_dir = path.dirname(path.realpath(__file__))

    from os import listdir
    sub_pkgs = []
    for dir_entry in listdir(pkg_dir):
        if dir_entry != "__init__.py" and dir_entry.endswith(".py"):
            full_path = path.join(pkg_dir, dir_entry)
            if path.isfile(full_path):
                sub_pkgs.append(dir_entry[:-3])
    __all__ = sub_pkgs

    # print(__all__)
