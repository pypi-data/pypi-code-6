import inspect
import os
import shutil


class FileUtils:

    def __init__(self):
        pass

    @staticmethod
    def delete_dirs(*paths):
        for path in paths:
            if os.path.isdir(path):
                shutil.rmtree(path)

    @staticmethod
    def delete_contents(location):
        for root, dirs, files in os.walk(location):
            for d in dirs:
                FileUtils.delete_dirs(os.path.join(root, d))
            for f in files:
                shutil.rmtree(os.path.join(root, f))

    @staticmethod
    def copy_contents(src, dst):
        if not os.path.isdir(src):
            return

        if not os.path.isdir(dst):
            os.mkdir(dst)

        for root, dirs, files in os.walk(src):
            for d in dirs:
                shutil.copytree(os.path.join(root, d), dst)
            for f in files:
                shutil.copyfile(os.path.join(root, f), os.path.join(dst, f))

    @staticmethod
    def to_absolute_path(relative_path):
        return os.path.normpath(os.path.join(os.path.dirname(__file__ ), '..', relative_path))

    @staticmethod
    def proj_folder():
        cur_script_folder = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        return os.path.split(cur_script_folder)[0]

    @staticmethod
    def conf_folder():
        return "{proj_dir}/conf".format(proj_dir=FileUtils.proj_folder())
