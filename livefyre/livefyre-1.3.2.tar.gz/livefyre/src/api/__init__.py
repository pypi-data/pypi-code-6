class Domain(object):
    @staticmethod
    def quill(core):
        try:
            ssl = core.ssl
        except AttributeError:
            ssl = core.network.ssl
        return 'https://{0}.quill.fyre.co'.format(core.get_network_name()) if ssl else 'http://quill.{0}.fyre.co'.format(core.get_network_name())
    
    @staticmethod
    def bootstrap(core):
        try:
            ssl = core.ssl
        except AttributeError:
            ssl = core.network.ssl
        return 'https://bootstrap.livefyre.com' if ssl else 'http://bootstrap.{0}.fyre.co'.format(core.get_network_name())


def get_lf_token_header(core, user_token = None):
    return {
            'Authorization': 'lftoken ' + (core.build_livefyre_token() if user_token is None else user_token),
            'Accepts': 'application/json'
    }
