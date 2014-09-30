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
            return tag.name, head_commit.hexsha
    return None, head_commit.hexsha


GET_VERSION_MAPPING = {
    'git': get_git_version,
}


def find_versions(repo_list):
    """
    Passing a list of tuples that consist of:

        ('reference_name', 'git', '/full/path/to/repo')

    Where:

    * reference_name can be anything and it will be yielded back in name

    * second element is the VCS type; for a list of supported VCS's see
      README.rst

    You receive a list of namedtuples:

        [
            (name='reference_name', tag='1.0', commit='fb666d55d3')
        ]

    :param repo_list: list of tuples as specified
    :return: list of namedtuples
    """
    for name, vcs_type, path in repo_list:
        vcs_type_normalized = vcs_type.lower()
        try:
            version_func = GET_VERSION_MAPPING[vcs_type_normalized]
        except KeyError as exc:
            raise version_info.exceptions.VCSNotSupported(exc.args[0])
        yield (name,) + version_func(path)
