from os import listdir
from os.path import join, isfile, isdir, abspath


def get_folder_content(folder):
    root = abspath(folder)
    return [join(root, x) for x in listdir(root)]


def get_files(folder):
    return [x for x in get_folder_content(folder) if isfile(x)]


def get_subfolders(folder):
    return [x for x in get_folder_content(folder) if isdir(x)]
