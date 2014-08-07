from pkg_resources import Requirement
from zc.buildout.easy_install import Installer


def get_newest_release(package_name, index=None):
    """Get the newest release version for a package from pypi.
    """
    installer = Installer(index=index)
    requirement = Requirement.parse(package_name)
    dist = installer._obtain(requirement)
    if dist:
        return dist.version
    else:
        return None
