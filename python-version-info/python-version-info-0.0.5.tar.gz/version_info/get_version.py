import collections

import git

import version_info.exceptions


__all__ = (
    'get_git_version',
    'find_versions',
)


VersionSpec = collections.namedtuple('VersionSpec', ['tag', 'commit'])


def get_git_version(path):
    repo = git.Repo(path)
    head_commit = repo.head.ref.commit
    for tag in repo.tags:
        if tag.commit == head_commit:
            return VersionSpec(tag.name, head_commit.hexsha)
    return VersionSpec(None, head_commit.hexsha)


GET_VERSION_MAPPING = {
    'git': get_git_version,
}


def find_versions(repo_list):
    """
    Passing a list of tuples that consist of:

        ('repo_one', 'git', '/full/path/to/repo_one')
        ('repo_two', get_version_callable, '/full/path/to/repo_two')

    Where:

    * first element can be anything and it will be yielded back as the first
      tuple element

    * second element is either:

        *  the VCS type as string;
           for a list of supported VCS's see README.rst

        *  a callable that will receive path and returns any object,
           but a namedtuple similar to VersionSpec is encouraged

    * third element is the path to the repository root or in case of
      custom callables any value that can explicitly define your repo

    You receive a generator where each element is a tuple of:

        ('repo_one', VersionSpec(tag='1.0', commit='fb666d55d3'))

    Casting the generator to a dictionary you can easily easily pass the
    version specs to your template engine:

        {
            'repo_one': VersionSpec(tag='1.0', commit='fb666d55d3'),
            'repo_two': CustomVersionSpec(version=(1,0,0))
        }

    :param repo_list: list of tuples as specified
    :return: generator of (name, VersionSpec) tuples
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
        yield name, version_func(path)
