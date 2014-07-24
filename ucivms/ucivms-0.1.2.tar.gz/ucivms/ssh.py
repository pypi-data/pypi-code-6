# This file is part of Ubuntu Continuous Integration virtual machine tools.
#
# Copyright 2014 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 3, as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
# SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

import os


from ucivms import subprocesses


def infos_from_path(key_path):
    """Analyze path to find ssh key type and kind.

    The basename should begin with ssh type used to create the key and end with
    '.pub' for a public key.

    If the type is neither of rds, dsa or ecdsa, None is returned.

    :param key_path: A path to an ssh key.

    :return: (type, kind) 'type' is the ssh key type or None if neither of rds,
        dsa or ecdsa. 'kind' is 'public' if the path ends with '.pub',
        'private' otherwise.
    """
    base = os.path.basename(key_path)
    for p in ('rsa', 'dsa', 'ecdsa'):
        if base.startswith(p):
            ssh_type = p
            break
    else:
        ssh_type = None
    if base.endswith('.pub'):
        kind = 'public'
    else:
        kind = 'private'
    return ssh_type, kind


def keygen(key_path, comment):
    """Generate an ssh keypair.

    :param key_path: The private path where the key should be generated (the
        public key path is obtained by adding the '.pub' suffix.

    :param comment: The comment to embed in the key for documentation and
        identification purposes.
    """

    ssh_type, kind = infos_from_path(key_path)
    path = os.path.expanduser(key_path)  # Just in case
    if kind == 'private':  # public will be generated at the same time
        subprocesses.run(['ssh-keygen', '-f', path, '-N', '', '-t', ssh_type,
                          '-C', comment])
