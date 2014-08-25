import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'quant.djangoapp.settings.main'

import quant.application

application = quant.application.Application()

