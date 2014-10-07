from db import db

__author__ = 'negash'


def get_kernel(database):
    configs = db.s('z', "SELECT * FROM pipeline_config." + database)

    if 'key' in configs[0]:
        tmp = {}
        for config in configs:
            tmp[config['key']] = config['value']
    else:
        tmp = []
        for config in configs:
            tmp.append(config['value'])
    return tmp