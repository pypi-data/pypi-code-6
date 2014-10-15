from bobsleigh.conf.handlers import InstallationHandler


class LocalHandler(InstallationHandler):
    "For my local development setup."

    def get_required_kwargs(self):
        return ('sitename',)

    def get_optional_kwargs(self):
        optional_kwargs = super(LocalHandler, self).get_optional_kwargs()
        optional_kwargs.update({
            'host': 'lanky',
        })
        return optional_kwargs

    def get_config_patterns(self):
        patterns = super(LocalHandler, self).get_config_patterns()
        patterns += (
            ('domain', '%(sitename)s.localhost'),
            ('db_name', '%(sitename)s'),
            ('db_user', '%(sitename)s'),
            ('log_path', '/var/log/django/%(sitename)s'),
            ('static_path', '/home/david/var/www/%(sitename)s/static'),
            ('media_path', '/home/david/var/www/%(sitename)s/uploads'),
            ('virtualenv_path', '/home/david/.virtualenvs/%(sitename)s'),
            ('project_path', '/home/david/www/%(sitename)s'),
        )
        return patterns


class VagrantHandler(InstallationHandler):
    "Geared up towards Vagrant machines."

    def get_required_kwargs(self):
        required_kwargs = super(VagrantHandler, self).get_required_kwargs()
        required_kwargs += 'sitename'
        return required_kwargs

    def get_optional_kwargs(self):
        optional_kwargs = super(LocalHandler, self).get_optional_kwargs()
        optional_kwargs.update({
            'host': 'precise32',
        })
        return optional_kwargs

    def get_config_patterns(self):
        patterns = super(LocalHandler, self).get_config_patterns()
        patterns += (
            ('domain', '%(sitename)s.vagrant'),
            ('db_name', '%(sitename)s'),
            ('db_user', '%(sitename)s'),
            ('log_path', '/var/log/django'),
            ('static_path', '/opt/site/static'),
            ('media_path', '/opt/site/uploads'),
            ('virtualenv_path', '/opt/site/.virtualenvs/site'),
            ('project_path', '/opt/site/django'),
        )
        return patterns
