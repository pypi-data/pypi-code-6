from django.conf import settings as djangosettings



class Settings():
    conf = djangosettings

    @property
    def BASE_DIR_NAME(self):
        return getattr(self.conf, 'DJANGO_MASTER_BASE_DIR', 'BASE_DIR')

    @property
    def BASE_DIR(self):
        return getattr(self.conf, self.BASE_DIR_NAME, None)

    @property
    def REQUIREMENTS_TXT(self):
        return getattr(self.conf, 'DJANGO_MASTER_REQUIREMENTS_NAME',
                       'requirements.txt')


settings = Settings()
