class VCSNotSupported(Exception):

    def __init__(self, vcs_type):
        self.message = '%s is not supported' % vcs_type
