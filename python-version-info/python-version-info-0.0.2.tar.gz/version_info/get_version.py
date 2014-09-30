import collections

import git

import version_info.exceptions


__all__ = (
    'get_git_version',
    'find_versions',
)


def get_git_version(path):
    repo = git.Repo(path)
    head_commit = repo.head.ref.commit
    for tag in repo.tags:
        if tag.commit == head_commit:
            return {
                'tag': tag.name,
                'commit': head_commit.hexsha
            }
    return {
        'tag': None,
        'commit': head_commit.hexsha
    }


GET_VERSION_MAPPING = {
    'git': get_git_version,
}


def find_versions(repo_list):
    """
    Passing a list of tuples that consist of:

        ('repo_one', 'git', '/full/path/to/repo_one')
        ('repo_two', get_version_callable, '/full/path/to/repo_two')

    Where:

    * reference_name can be anything and it will be yielded back in name

    * second element is either:

        *  the VCS type as string;
           for a list of supported VCS's see README.rst

        *  a callable that will receive path and returns a dict
           containing virtually any values, except for 'name' and
           reserved Python words such as def or class

    You receive a list of namedtuples:

        [
            (name='reference_name', tag='1.0', commit='fb666d55d3')
            (name='reference_name', dict_value_one=1, dict_value_two=2)
        ]

    :param repo_list: list of tuples as specified
    :return: list of namedtuples
    """
    for name, vcs_type, path in repo_list:
        if callable(vcs_type):
            version_func = vcs_type
        else:
            vcs_type_normalized = vcs_type.lower()
            try:
                version_func = GET_VERSION_MAPPING[vcs_type_normalized]
            except KeyError as exc:
                raise version_info.exceptions.VCSNotSupported(exc.args[0])
        version_spec = version_func(path)
        version_spec_keys = ['name', ] + version_spec.keys()
        version_spec_values = [name, ] + version_spec.values()
        version_spec_class = collections.namedtuple('VersionSpec',
                                                    version_spec_keys)
        yield version_spec_class(*version_spec_values)
