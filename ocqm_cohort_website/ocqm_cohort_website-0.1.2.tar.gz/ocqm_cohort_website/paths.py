import os
import shutil


def get_module_path():
    return os.path.join(
        *os.path.split(
            os.path.join(os.path.realpath(__file__))
        )[:-1]
    )


def get_theme_path():
    return os.path.join(get_module_path(), 'theme')


def get_static_path():
    return os.path.join(get_theme_path(), 'media')


def get_locale_path():
    return os.path.join(get_module_path(), 'locale')


def get_example_path():
    return os.path.join(get_module_path(), 'example')


def copy_files(src, dest):
    if os.path.isdir(src):
        if not os.path.isdir(dest):
            os.makedirs(dest)

        for f in os.listdir(src):
            copy_files(os.path.join(src, f), os.path.join(dest, f))
    else:
        shutil.copyfile(src, dest)


def ensure_directory(path):
    if not os.path.exists(path):
        os.mkdir(path)
    else:
        assert os.path.isdir(path)
