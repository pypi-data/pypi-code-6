# -*- coding: utf-8 -*-


from fabric.api import *


def config_nginx(local_name, remote_name):
    """
    directory must be ./config/nginx/*.conf
    """
    put('./config/nginx/{}.conf /etc/nginx/conf.d/{}.conf'.format(local_name, remote_name))


def config_supervisor(local_name, remote_name):
    """
    directory must be ./config/supervisor.d/*.ini
    """
    put('./config/supervisord/{}.ini /etc/supervisor.d/{}.ini'.format(local_name, remote_name))



