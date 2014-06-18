from vdt.versionplugin.debianize import get_version

def set_version(version):
    """
    Never change the version.
    """
    return get_version(version.extra_args)