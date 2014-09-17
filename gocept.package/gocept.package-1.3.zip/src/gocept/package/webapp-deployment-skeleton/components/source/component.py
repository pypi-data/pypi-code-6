from batou import UpdateNeeded
from batou.lib.file import Symlink, Directory
from batou.lib.mercurial import Clone
import batou.component
import os.path


class Source(batou.component.Component):
    """Manage any VCS working copies being worked on in this deployment.

    ``sources`` point to source code of Python eggs, ``checkouts`` to anything
    else. Assuming mercurial as the only VCS being used, the line format is

    https://example.org/path/to/project#branch

    where the branch is optional and the last portion of the URL path is used
    as the project name inside the ``source`` component.

    """

    sources = """\
""".split()

    checkouts = """\
""".split()

    def configure(self):
        self.require('hgrc', self.host)
        self.paths = []
        self.provide('source', self)
        self.source_names = [self.add_clone(url) for url in self.sources]
        for url in self.checkouts:
            self.add_clone(url)

    __update_needed = None

    def verify(self):
        # This check incurs network access for each source checkout, so we
        # want to short-cut repeated calls.
        if self.__update_needed is None:
            try:
                super(Source, self).verify()
            except UpdateNeeded:
                self.__update_needed = True
            else:
                self.__update_needed = False
        if not self.__update_needed:
            raise UpdateNeeded()

    def add_clone(self, url):
        name, _, branch = url.rpartition('/')[2].partition('#')
        clone = Clone(url, branch=(branch or 'default'), target=name)
        self += clone
        return name

    @property
    def mr_developer(self):
        result = []
        for name in self.source_names:
            result.append('{0} = fs {0}'.format(name))
        return '\n'.join(result)

    def add_symlinks_to(self, other):
        other += Directory(other.sources_dir)
        for name in self.source_names:
            other += Symlink(os.path.join(other.sources_dir, name),
                             source=os.path.join(self.workdir, name))
