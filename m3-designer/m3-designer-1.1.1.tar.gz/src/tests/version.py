#coding:utf-8

import os

project_path = os.path.dirname(__file__)

__version__ = '1.0'
__appname__ = u'Тестовое приложение для m3_designer'

__require__ = {
    'm3': '1.0',
}

# исходные тексты m3_plugins всегда забираем локально из текущего репозитория
# поэтому путь такой вот
__require_local__ = {
    'm3_designer': os.path.realpath(os.path.join(project_path, '../../')),
}
