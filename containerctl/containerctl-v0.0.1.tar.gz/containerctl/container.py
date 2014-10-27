"""Manage containers."""
import os
import pystache
import subprocess
import yaml
from .errors import ConfigError, ContainerError

config_defaults = {
    'user': None,
    'name': None,
    'prebuild': None,
    'path': None,
    'fig': None,
}


def read_config(configfile):
    """
    Return container configuration from a file. See `Container.from_path` for a description of the
    config file syntax.
    """
    try:
        with open(configfile) as f:
            filedata = yaml.load(f)
    except IOError as e:
        raise ConfigError("failed to open '{}': {}".format(configfile, e))
    except yaml.YAMLError as e:
        raise ConfigError("failed to parse '{}': {}".format(configfile, e))

    config = config_defaults.copy()
    config.update(filedata)

    name = config['name']
    if not name:
        raise ConfigError("name is empty or missing")
    if not isinstance(name, (str, unicode)):
        raise ConfigError("name must be a string")
    if '/' in name:
        config['user'], config['name'] = name.split('/', 1)

    for key in ('user', 'name', 'prebuild', 'path'):
        if config[key] is not None and not isinstance(config[key], (str, unicode)):
            raise ConfigError("{} must be a string".format(config, key))

    if config['fig'] is not None and not isinstance(config['fig'], dict):
        raise ConfigError("fig must be a dictionary")

    return config


class Container(object):
    """Manage a container."""

    @classmethod
    def from_path(cls, path=None, **override):
        """
        Return a container found at the provided directory `path`. Expects a `container.yml` to
        exist in `path`. If `path` is `None` (the default) the output of `os.getcwd()` will be used
        for `path`.

        The config file must contain valid YAML. Valid keys are:

        * `path` - The path to the directory containing that container's Dockerfile and other
            configuration. This is set to the `path` value determined by this function if absent
            from the config file.
        * `user` - The user part of the container's full tag.
        * `name` - The name part of the container's full tag. If this value contains a `/` it will
            be stripped of the string up to and including the `/`. The `user` value will be set to
            the stripped portion exclufing the `/`. This will override any value explicitly set in
            `user`.
        * `prebuild` - A script to run before calling `docker build` on the container.
        * `fig` - A fig cofiguration to use when running the container.

        The `prebuild` and `fig` values may have values substituted using the Mustache template
        syntax. Valid substitutions are `name`, `user`, `version`, and `tag`.

        An example may look like this:

            name: nginx
            prebuild: ./prebuild {{version}}
            fig:
                site:
                    image: example/site
                nginx:
                    image: {{tag}}
                    ports:
                    - 80
                    volumes_from: site

        Config values may be passed as keyword arguments. In this case they override the values
        provided in the config file.

        A `ConfigError is raised if: `path` is not a directory; a single container configuration is
        expected and zero or more than one are found; no config file is found; or the config file
        is invalid.

        A `ContainerError` may be raised by `__init__` which is called in this method.
        """
        if path is None:
            path = os.getcwd()
        if not os.path.isdir(path):
            raise ConfigError("path '{}' is not a directory".format(path))

        configfile = os.path.join(path, 'container.yml')
        if not os.path.isfile(configfile):
            raise ConfigError("config file '{}' not found".format(configfile))

        config = read_config(configfile)
        if config.get('path') is None:
            config['path'] = path
        config.update(override)
        return cls.from_dict(config)

    @classmethod
    def from_dict(cls, data):
        """Build a container object from a dictionary."""
        return cls(
            data.get('path'),
            data.get('user'),
            data.get('name'),
            data.get('version'),
            data.get('prebuild'),
            data.get('fig'),
        )

    def __init__(self, path, user, name, version=None, prebuild=None, fig=None):
        """
        Initialize the container. The `path` should be a directory containing the container's
        Dockerfile. The `user` and `name` is combined to create the image repo. The `name` should
        match the directory containing the container's Dockerfile.

        The `version` value is used to tag the container on build. If `version` is `None` the
        version will be detected using `containerctl.version.detect`.

        The `prebuild` param is a command to run before calling `docker build` on the container. If
        `prebuild` is `None` and an executable file called `prebuild` exists in `path` it will be
        executed as the prebuild script.

        If the `fig` value is provided it will be written as YAML to be used as the fig
        configuration when running this container. Otherwise a very simple fig.yml file will be
        written to execute the container.
        """
        def aslist(val):
            if isinstance(val, (list, tuple)):
                return list(val)
            return [val]

        if not name:
            raise ContainerError("container name must not be empty")
        if not os.path.isdir(path):
            raise ContainerError("container {} has invalid path '{}'".format(name, path))

        self.path = os.path.abspath(path)
        self.user = user
        self.name = name

        self._version = version
        self._prebuild = prebuild
        self._fig = fig

        if not self.name:
            raise ContainerError("container has no name")

    def to_dict(self, raw=False):
        """
        Return the container as a dictionary. If `raw` is `True` then the un-evaluated
        configuraiton is returned.
        """
        def rel(base, path):
            if path and path.startswith(base):
                path = '.' + path[len(base):]
            return path

        cwd = os.getcwd()
        if raw:
            data = {'name': self.name}
            if self.user:
                data['user'] = self.user
            if self._version:
                data['version'] = self._version
            if self._prebuild:
                data['prebuild'] = self._prebuild
            if self._fig:
                data['fig'] = self._fig

            path = rel(cwd, self.path)
            if path and path != '.':
                data['path'] = path
        else:
            data = {
                'tag': self.tag,
                'user': self.user,
                'name': self.name,
                'version': self.version,
                'fig': self.fig,
                'built': self.built,
                'running': self.running,
            }
            path = rel(cwd, self.path)
            if path and path != '.':
                data['path'] = path
            prebuild = rel(cwd, self._get_prebuild())
            if prebuild and prebuild != '.':
                data['prebuild'] = prebuild
        return data

    def to_config(self):
        """Return the container's configuration."""

    def _exec(self, args, check=False, quiet=False):
        """
        Run an executable. If `check` is `True` raises a ContainerError on call failure. If `quiet`
        is `False` then I/O is redirected to /dev/null.
        """
        if quiet:
            with open(os.devnull, 'w') as devnull:
                ret = subprocess.call(args, stderr=devnull, stdout=devnull, stdin=devnull)
        else:
            ret = subprocess.call(args)

        if check and ret != 0:
            raise ContainerError("exec failed for {}: {}".format(self.name, args))
        return ret

    def _format(self, value):
        """
        Format a string value with the `user`, `name`, `version`, and `tag`. Keyword args may be
        provided to override these values or add additonal values for substitution.
        """
        if not value:
            return ''
        return pystache.render(value, {
            'user': self.user or '',
            'name': self.name or '',
            'version': self.version or '',
            'tag': self.tag,
        })

    def _get_prebuild(self):
        """Return the prebuild command."""
        if self._prebuild:
            return self._format(self._prebuild)
        else:
            cmd = os.path.join(self.path, 'prebuild')
            if os.path.isfile(cmd) and os.access(cmd, os.X_OK):
                return cmd
        return None

    @property
    def version(self):
        """
        Return the container version. Executes version detection if necessary. Raises
        `VersionError` on detection failure.
        """
        if self._version:
            return self._version
        from .version import detect
        return detect(self)

    def _get_fig(self):
        """Return the formatted fig configuration."""
        def fmt(data):
            res = {}
            for k, v in data.iteritems():
                if isinstance(v, (str, unicode)):
                    res[k] = self._format(v)
                elif isinstance(v, dict):
                    res[k] = fmt(v)
                else:
                    res[k] = v
            return res
        return fmt(self._fig)

    def _write_fig(self):
        """Write the fig configuration to `fig.yml`."""
        configfile = os.path.join(self.path, 'fig.yml')
        try:
            with open(configfile, 'w') as f:
                fig = self._get_fig()
                f.write(yaml.safe_dump(fig, explicit_start=False, default_flow_style=False))
        except IOError:
            raise ContainerError("unable to write to '{}'".format(configfile))
        except yaml.YAMLError as e:
            raise ContainerError("failed to encode config: {}", e)

    @property
    def fig(self):
        """Return the formatted fig configuration."""
        return self._get_fig()

    @property
    def tag(self):
        """Return the full container tag."""
        tag = self.name
        if self.user:
            tag = '/'.join((self.user, tag))
        version = self.version
        if version:
            tag = ':'.join((tag, version))
        return tag

    @property
    def dockerfile(self):
        """Return the expected path to the Dockerfile for this container."""
        return os.path.join(self.path, 'Dockerfile')

    @property
    def built(self):
        """
        Return True if the container has been built previously. This does not guarantee that the
        existing image is up to date.
        """
        with open(os.devnull, 'w') as devnull:
            code = subprocess.call(['docker', 'inspect', self.tag],
                                   cwd=self.path, stderr=devnull,
                                   stdout=devnull, stdin=devnull)
            return code == 0

    def prebuild(self):
        """Execute container prebuild step."""
        cmd = self._get_prebuild()
        if not cmd:
            return

        env = os.environ.copy()
        env = env.update({
            'CONTAINER_PATH': self.path,
            'CONTAINER_USER': self.user,
            'CONTAINER_NAME': self.name,
            'CONTAINER_VERSION': self.version,
            'CONTAINER_TAG': self.tag,
        })

        try:
            subprocess.check_call(["bash", "-c", cmd], cwd=self.path, env=env)
        except subprocess.CalledProcessError:
            raise ContainerError("{} prebuild failed".format(self.tag))

    def build(self, prebuild=None, nocache=None):
        """
        Build the container. If `prebuild` is `True` (the default) the container's prebuild scripts
        are run. The Docker cache may be invalidated prior to the build by setting `nocache` to
        `True`.

        Raises `ContainerError` on failure.
        """
        if prebuild is None:
            prebuild = True
        if nocache is None:
            nocache = False

        if not os.path.exists(self.dockerfile):
            raise ContainerError("{} build failed: no Dockerfile".format(self.tag)) 
        if prebuild:
            self.prebuild()
        args = ['docker', 'build', '--force-rm', '--rm', '-t', self.tag]
        if nocache:
            args.append('--no-cache')
        args.append('.')
        try:
            subprocess.check_call(args, cwd=self.path)
        except subprocess.CalledProcessError:
            msg = "{} build failed: docker returned non-zero exit code"
            raise ContainerError(msg.format(self.tag))

    def push(self):
        """Push the built container to its registry."""
        if not self.built:
            raise ContainerError("{} push failed: image not built".format(self.name))
        try:
            subprocess.check_call(['docker', 'push', self.tag], cwd=self.path)
        except subprocess.CalledProcessError:
            raise ContainerError("{} push failed: docker returned non-zero exit code")

    def remove(self):
        """
        Remove the container from docker. Raise a ContainerError if the remove fails.
        """
        try:
            subprocess.check_call(['docker', 'rmi', self.tag], cwd=self.path)
        except subprocess.CalledProcessError:
            raise ContainerError("{} remove failed")

    @property
    def running(self):
        """Return True if the container is running."""
        try:
            out = subprocess.check_output(['fig', 'ps', '-q'], cwd=self.path).strip()
            if out:
                return True
            return False
        except subprocess.CalledProcessError:
            raise ContainerError("{} running check failed")

    def run(self, detach=None):
        """
        Run the container. Calls `fig up` to start the container and its dependencies. As such fig
        and a fig.yml are required to be present. After running the containers are removed using
        `fig rm`. If `detach` is set to `True` then the containers will be run in the background.
        They must be stopped by calling `kill` for the `fig rm` cleanup to take place.
        """
        self._write_fig()
        try:
            args = ['fig', 'up']
            if detach:
                args.append('-d')
            subprocess.check_call(args, cwd=self.path)
        except subprocess.CalledProcessError:
            raise ContainerError("{} run failed")
        finally:
            if not detach:
                subprocess.call(['fig', 'rm', '--force', '-v'], cwd=self.path)

    def kill(self):
        """
        Kill the running container. Calls `fig kill` to stop the container and its dependencies.
        Once stopped a `fig rm` is issued to clean up the stopp containers.
        """
        try:
            if self.running:
                subprocess.check_call(['fig', 'kill'], cwd=self.path)
        except subprocess.CalledProcessError:
            raise ContainerError("{} kill failed")
        finally:
            subprocess.call(['fig', 'rm', '--force', '-v'], cwd=self.path)
