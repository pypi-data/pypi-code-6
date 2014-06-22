#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os
import tarfile


def create_tarball(dirs_to_tarball, tarball_name, save_dir,
                   backup_date_fmt="%Y%m%d_%H%M%S", gzip=True):
    if gzip:
        tar_opts = 'w:gz'
        file_suffix = 'tar.gz'
    else:
        tar_opts = 'w:'
        file_suffix = 'tar'

    if backup_date_fmt:
        utcnow = datetime.datetime.utcnow()
        tarball_filename = "{0}_{1}.{2}".format(
            tarball_name,
            utcnow.strftime(backup_date_fmt),
            file_suffix)
    else:
        tarball_filename = "{0}.{1}".format(
            tarball_name,
            file_suffix)

    tarball_filepath = os.path.join(save_dir, tarball_filename)

    try:
        tar = tarfile.open(tarball_filepath, tar_opts)
        for dir in dirs_to_tarball:
            tar.add(dir)
    except:  # pragma: no cover
        return False
    finally:
        tar.close()

    if tarfile.is_tarfile(tarball_filepath):
        return tarball_filepath
    else:
        return None


# vim: filetype=python
