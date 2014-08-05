import os
import tarfile
import shutil
import re
from contextlib import closing

def generate_lesson_tarball(path):
    dist_path = os.path.join(path, "dist")
    if os.path.isdir(dist_path):
        shutil.rmtree(dist_path)
    os.mkdir(dist_path)
    tarball_path = os.path.join(dist_path, "lesson.tar.gz")

    exclude_files = [".+\.pyc$"]
    with closing(tarfile.open(tarball_path, "w:gz")) as tar:
        for (dirpath, dirnames, filenames) in os.walk(path):
            exclude_dirs = [
                ".git",
                "node_modules",
                "bower_components",
                "coverage",
                ".tox"]
            dirnames[:] = [d for d in dirnames if d not in exclude_dirs]

            for filename in filenames:
                if any(re.match(regexp, filename) for regexp in exclude_files):
                    continue
                tar.add(os.path.join(dirpath, filename), arcname=os.path.join(dirpath.replace(path, ""), filename))
    return tarball_path
