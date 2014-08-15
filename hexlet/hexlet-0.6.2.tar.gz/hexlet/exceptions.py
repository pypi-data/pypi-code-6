class Error(Exception):
    pass


class ConfigError(Error):
    pass


class ManifestError(Error):
    pass

class VersionUpdateError(Error):
    def __init__(self, message):
        self.message = message
