#!/usr/bin/env python
"""
<description>

This file is part of ZTC and distributed under the same license.
http://bitbucket.org/rvs/ztc/

Copyright (c) 2011 Vladimir Rusinov <vladimir@greenmice.info>
"""

import time

from ztc.check import ZTCCheck, CheckFail
from ConfigParser import ConfigParser
import ztc.lib.flup_fcgi_client as fcgi_client

class PHPFPMCheck(ZTCCheck):
    name = "php-fpm"
    
    OPTPARSE_MIN_NUMBER_OF_ARGS = 1
    OPTPARSE_MAX_NUMBER_OF_ARGS = 2
    
    
    def _myinit(self):
        self.fpm_config_path = self.config.get('fpm_config', '/etc/php5/fpm/pool.d/www.conf')
        self.fpmconfig = ConfigParser()
        self.fpmconfig.read(self.fpm_config_path)
    
    
    def _get(self, metric, *arg, **kwarg):
        if metric == 'ping':
            return self.ping
        elif metric == 'status':
            m = arg[0]
            return self.get_status(m)
        else:
            raise CheckFail("unknown metric")
    
    
    def _detect_fpm_configuration(self):
        """ trying to parse php-fpm config """
        return fpmconfig
    
    
    def _load_page(self, section, url):
        """ load fastcgi page """
        try:
            listen = self.fpmconfig.get(section, 'listen')
            if listen[0] == '/':
                #it's unix socket
                fcgi = fcgi_client.FCGIApp(connect = listen)
            else:
                if listen.find(':') != -1:
                    _listen = listen.split(':')
                    fcgi = fcgi_client.FCGIApp(host = _listen[0], port = _listen[1])
                else:
                    fcgi = fcgi_client.FCGIApp(port = listen, host = '127.0.0.1')

            env = {
               'SCRIPT_FILENAME': url,
               'QUERY_STRING': '',
               'REQUEST_METHOD': 'GET',
               'SCRIPT_NAME': url,
               'REQUEST_URI': url,
               'GATEWAY_INTERFACE': 'CGI/1.1',
               'SERVER_SOFTWARE': 'ztc',
               'REDIRECT_STATUS': '200',
               'CONTENT_TYPE': '',
               'CONTENT_LENGTH': '0',
               #'DOCUMENT_URI': url,
               'DOCUMENT_ROOT': '/',
               'DOCUMENT_ROOT': '/var/www/'
               }
            ret = fcgi(env)
            return ret
        except:
            self.logger.exception('fastcgi load failed')
            return '500', [], '', ''
    
    
    @property
    def ping(self):
        """ calls php-fpm ping resource """
        if len(self.fpmconfig.sections()) == 0:
            self.logger.error('Can\'t read from PHP-FPM config')
        else:
            for pool_name in self.fpmconfig.sections():
                if not self.fpmconfig.has_option(pool_name, 'ping.path'):
                    self.logger.error('Ping path is not configured for pool ' + pool_name)
                else:
                    st = time.time()
                    code, headers, out, err = self._load_page(pool_name, self.fpmconfig.get(pool_name, 'ping.path'))
                    if code.startswith('200') and out == 'pong':
                        return time.time() - st
                    else:
                        self.logger.error('ping: got response, but not correct')
                        return 0
    
    
    def get_status(self, metric):
        """ get php-fpm status metric """
        metric = metric.replace('_', ' ')
        
        page = self.get_status_page()
        if not page:
            raise CheckFail("unable to get status page")
        for line in page.splitlines():
            if line.startswith(metric):
                return line.split()[-1]
        # no such metric found
        raise CheckFail("no such metric found")
    
    
    def get_status_page(self):
        """ return php-ftm status page text """
        if len(self.fpmconfig.sections()) == 0:
            self.logger.error('Can\'t read from PHP-FPM config')
        else:
            for pool_name in self.fpmconfig.sections():
                if not self.fpmconfig.has_option(pool_name, 'pm.status_path'):
                    self.logger.error('Status path is not configured for pool ' + pool_name)
                else:
                    code, headers, out, err = self._load_page(pool_name, self.fpmconfig.get(pool_name, 'pm.status_path'))
                    if code.startswith('200'):
                        return out
                    else:
                        self.logger.error('status: got response, but not correct')
                        return None
