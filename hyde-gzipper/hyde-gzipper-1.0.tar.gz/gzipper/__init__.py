from hyde.plugin import Plugin
import gzip

class GzipperPlugin(Plugin):
    """
    A Hyde plugin for putting gzipped versions alongside output resources.
    Default configuration:

    gzipper:
        extensions:
            - html
            - css
            - js
    """

    def begin_site(self):
        self.files = []
        try:
            self.exts = set(self.site.config.gzipper.extensions)
        except AttributeError:
            self.exts = set(['html', 'css', 'js'])

    def text_resource_complete(self, resource, text):
        self.binary_resource_complete(resource)
        return text

    def binary_resource_complete(self, resource):
        deploy_path = self.site.config.deploy_root_path.child(resource.get_relative_deploy_path())
        ext = deploy_path.rsplit('.', 1)[-1]
        if ext in self.exts:
            self.files.append(deploy_path)

    def generation_complete(self):
        for deploy_path in self.files:
            self.logger.debug('Gzipping resource path [%s]' % (deploy_path,))
            with open(deploy_path, 'rb') as source:
                with gzip.open(deploy_path + '.gz', 'wb') as target:
                    while True:
                        data = source.read(1<<20)
                        if not data: break
                        target.write(data)

