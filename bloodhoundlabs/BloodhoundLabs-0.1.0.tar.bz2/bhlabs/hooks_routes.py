#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright 2013 Olemis Lang <olemis at gmail.com>
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


r"""Apache(TM) Bloodhound extensions

Web bootstrap handlers powered by Routes middleware.

Copyright 2013 Olemis Lang <olemis at gmail.com>
Licensed under the Apache License
"""

import os.path
from routes import Mapper
from routes.middleware import RoutesMiddleware

from trac.config import ChoiceOption, Option
from trac.core import Component, implements
from trac.env import open_environment
from trac.hooks import BootstrapHandlerBase
from trac.resource import IResourceChangeListener
from trac.web.api import HTTP_STATUS, RequestDone
from trac.web.main import get_environments, RequestWithSession, \
                          send_project_index

from multiproduct.env import ProductEnvironment
from multiproduct.model import Product

__all__ = ['ProductRoutesBootstrapHandler', 'bootstrap_product_subdomain',
           'bootstrap_sibling_products', 'bootstrap_embedded_products',
           'helper_bootstrap_subdomain', 'helper_bootstrap_siblings']


class ProductRoutesBootstrapHandler(BootstrapHandlerBase):
    """Load environment based on Routes middleware.
    """
    @staticmethod
    def VOID_WSGI_APP(environ, start_response):
        return lambda data : None

    def __init__(self, mapper=None):
        """Initialize this instance

        :param mapper: optional instance of `routes.Mapper`
        :param use_method_override: 
        """
        self.mapper = mapper or Mapper()
        self._mw = RoutesMiddleware(self.VOID_WSGI_APP, self.mapper,
                                    use_method_override=False, singleton=False)

    def open_environment(self, environ, start_response):
        """Lookup routes matching the target WSGI environment dictionary.
        Match results will be used as follows:

          - `controller` will be ignored
          - `envname` will be the name of the target Trac environment
            used e.g. to select environment folder when 
            TRAC_ENV_PARENT_DIR is set and also to determine authentication
            domains while running TracStandalone server (but not limited
            to those use cases). This entry will be ignored on single
            environment deployments .
          - `product` target product prefix. Used to load a product environment
            and dispatch the request in product context. If missing or empty
            the target will be the global environment
          - `error_status` HTTP status code returned on error (default=500)
          - `error_reason` HTTP response body on error
          - `action` will be one of the following supported values
            * `dispatch` will trigger request handler dispatching loop
              in the context of the target (Trac | product) environment
            * `envlist` will display environment index page
              ( see wiki:TracInterfaceCustomization#ProjectList ).
              All variables mentioned above will be ignored.
            * `error` will return an HTTP error back to the client
              (see `error_*` variables above)
          - `path_info` : see [http://routes.readthedocs.org/en/latest/setting_up.html#magic-path-info Routes magic path info]

        If no match is detected then it defaults to `{action : 'envlist'}` .
        """
        # Apply routes side-effects
        env_path = environ.get('trac.env_path')
        self._mw(environ, self.VOID_WSGI_APP)
        match = ( environ.get('wsgiorg.routing_args') or 
                  (None, dict(action='envlist')) )[1]

#        log = environ.get('wsgi.errors')
#        if log:
#            log.write("[BH Labs] Routes match " + repr(match))

        action = match.get('action', 'envlist')

        if env_path:
            environ['trac.env_name'] = os.path.basename(env_path)
        elif match:
            env_parent_dir = environ.get('trac.env_parent_dir')
            env_paths = environ.get('trac.env_paths')
            if env_parent_dir or env_paths:
                # The value of 'envname' in routes match is the base name of
                # the environment
                env_name = match.get('envname')

                if action == 'dispatch':
                    if not env_name:
                        self._send_http_error(environ, start_response, 500,
                                              'Missing environment name')
                    # See further processing below
                elif action == 'envlist':
                    # No specific environment requested, so render an 
                    # environment index page
                    send_project_index(environ, start_response, env_parent_dir,
                                       env_paths)
                    raise RequestDone
                elif action == 'error':
                    status = match.get('error_status', 500)
                    try:
                        status = int(status)
                    except ValueError:
                        status = 500
                    self._send_http_error(environ, start_response, 
                                          status, match.get('error_reason'))
                else:
                    self._send_http_error(environ, start_response, 500,
                                          "Unsupported action '%s' in "
                                          "bootstrap routes" % (action,) )

                environ['trac.env_name'] = env_name

                if env_parent_dir:
                    env_path = os.path.join(env_parent_dir, env_name)
                else:
                    env_path = get_environments(environ).get(env_name)

                if not env_path or not os.path.isdir(env_path):
                    errmsg = 'Environment not found'
                    self._send_http_error(environ, start_response,
                                          reason=errmsg)

        if not env_path:
            reason = 'The environment options "TRAC_ENV" or ' \
                     '"TRAC_ENV_PARENT_DIR" or the mod_python ' \
                     'options "TracEnv" or "TracEnvParentDir" are ' \
                     'missing. Trac requires one of these options ' \
                     'to locate the Trac environment(s).'
            self._send_http_error(environ, start_response, 500, reason)

        run_once = environ['wsgi.run_once']

        env = open_environment(env_path, use_cache=not run_once)
        # Ensure env._abs_href is set
        abs_href = env.abs_href
        product_id = match.get('product')
        if product_id:
            try:
                env = ProductEnvironment(env, product_id)
            except LookupError:
                errmsg = "Unknown product '%s'" % (product_id)
                self._send_http_error(environ, start_response, reason=errmsg)
        return env

    def probe_environment(self, environ):
        """Apply routes side-effects upon WSGI `environ`
        """
        # Apply routes side-effects
        env_path = environ.get('trac.env_path')
        self._mw(environ, self.VOID_WSGI_APP)
        match = ( environ.get('wsgiorg.routing_args') or 
                  (None, dict(action='envlist')) )[1]
        action = match.get('action', 'envlist')

        # Update 'trac.env_name'
        if env_path:
            environ['trac.env_name'] = os.path.basename(env_path)
        elif match:
            env_parent_dir = environ.get('trac.env_parent_dir')
            env_paths = environ.get('trac.env_paths')
            if env_parent_dir or env_paths:
                # The value of 'env_name' in routes match is the base name of
                # the environment
                environ['trac.env_name'] = match.get('envname')

    def create_request(self, env, environ, start_response):
        req = RequestWithSession(environ, start_response)
        # Patch needed to be compatible with ProductizedHref
        req.href._global_href = req.href
        req.abs_href._global_href = req.abs_href
        return req

    def _send_http_error(self, environ, start_response, status=404, reason=None):
        status_line = '%s %s' % (status, HTTP_STATUS.get(status, 'Unknown'))
        if not reason:
            reason = '%s (%s)' % (HTTP_STATUS.get(status, 'Unknown'), status)
        write = start_response(status_line,
                       [('Content-Type', 'text/plain'),
                        ('Content-Length', str(len(reason)))])
        write(reason)
        raise RequestDone

    DEFAULT_MATCH_ERROR = dict(error_status=404,
                               error_reason='Not found (no route to target)')


#-------------------------
# Common product resource namespaces
# https://issues.apache.org/bloodhound/wiki/Proposals/BEP-0003#url-mapping
#-------------------------

# Product sub-domain namespace
# https://issues.apache.org/bloodhound/wiki/Proposals/BEP-0003#deploy-domain
# https://issues.apache.org/bloodhound/wiki/Proposals/BEP-0003#deploy-domain-path

def helper_bootstrap_subdomain(b=None, depth=2, global_subdomain=None,
                               base_path=None):
    """Setup Routes bootstrap handler to serve product data in sub-domains.
    Environment names must match target domain name. Product subdomains
    are hosted at the same level in sibling sub-domains.

    :param b:     Optional instance of `ProductRoutesBootstrapHandler`. This
                  parameter serves to the purpose of applying sub-domain routes
                  after connecting an initial set of routes
    :param depth: Optional numeric value used to determine the boundary between
                  domain (i.e. environment) name and sub-domain (i.e. product)
                  name.
                  e.g. `depth=2` for p1.domain.tld, p2.domain.tld, ...
                  e.g. `depth=3` for p1.x.y.tld, p2.x.y.tld, p1.x.z.tld ...
    :param global_subdomain: Optional string value for special sub-domain name
                  for global environment.
                  It may also be a callable object with a signature satisfying
                  the following contract

                  :param raw_env_name: list with matched domain names in order
                  :param product: matched product name (string) or `None`
                  :return: a binary tuple (raw_env_name, product) to override
                           previous match or None to stick with it

    :param base_path: Optional path prefix to Bloodhound URL namespace

    Notice: There is no URL mapping for environments index page
    """
    if depth < 2:
        # At least match top-level and second-level domain identifiers
        raise ValueError("Domains depth must be greater than 2")

    _global_subdomain = None
    if not global_subdomain:
        pass
    elif isinstance(global_subdomain, basestring):
        _global_subdomain = (lambda raw_env_name, product : (raw_env_name, None)
                                if product == global_subdomain else None)
    elif isinstance(global_subdomain, dict):
        _global_subdomain = (lambda raw_env_name, product : (raw_env_name, None)
                                if product == global_subdomain.get(
                                                            tuple(raw_env_name))
                                else None)
    elif callable(global_subdomain):
        def _global_subdomain(raw_env_name, product):
            # FIXME : Paranoia vs performance
            try:
                return global_subdomain(raw_env_name, product)
            except:
                return None

    def sub_domain_condition(environ, result):
        """Extract environment and product name from HTTP `Host` header.
        """
        host = environ.get('HTTP_HOST', '')
        domain_parts = host.split('.')
        if 0 <= len(domain_parts) - depth <= 1:
            env_name = domain_parts[-depth:]
            product = domain_parts[:-depth]
            product = product[0] if product else None
            if _global_subdomain is not None:
                override = _global_subdomain(env_name, product)
                if override is not None:
                    env_name, product = override
            if product:
                result['product'] = product
            result['envname'] = '.'.join(env_name)
            result['action'] = 'dispatch'
        else:
            result['action'] = 'error'
            result['error_status'] = '404'
            result['error_reason'] = 'Unknown host ' + host
        return True

    b = b or ProductRoutesBootstrapHandler()
    base_path = base_path or u''
    b.mapper.connect(None, base_path + u'/{path_info:.*}',
                     conditions={'function' : sub_domain_condition})
    return b

bootstrap_product_subdomain = helper_bootstrap_subdomain()


class ProductDomainRegistrar(Component):
    """Update DNS records for (sub)domains on product creation

    This class is used in combination with bootstrap handlers instantiated by
    `helper_bootstrap_subdomain` e.g. `bootstrap_product_subdomain`
    """
    implements(IResourceChangeListener)

    tsig_key = Option('dns', 'tsig_key', '',
        """DNS server authentication key""")

    tsig_keyname = Option('dns', 'tsig_keyname', '',
        """DNS server authentication key name""")

    dns_server_host = Option('dns', 'host', 'localhost',
        """DNS server host name""")

    dns_type = ChoiceOption('dns', 'record_type', ['CNAME', 'A'],
        """DNS record type i.e. one of `CNAME` (default) or `A`""")

    dns_value = Option('dns', 'record_value', '',
        """DNS record value (defaults to parent domain for CNAME)""")

    # IResourceChangeListener methods

    def match_resource(self, resource):
        """Match product resources
        """
        return isinstance(resource, Product)

    def resource_created(self, resource, context):
        """Create DNS entry for (sub)domain once product is created.
        Parent domain will be retrieved from environment (folder) path name.
        """
        self.log.debug("Attempt DNS zone edit for product %s", resource.prefix)
        try:
            import dns
        except ImportError:
            self.log.error("[DNS] Error: Unable to import module 'dns'")
            return
        if not (self.tsig_key and self.tsig_keyname):
            self.warning('[DNS] Invalid config: DNS server access tokens')
        else:
            global_env = self.env.parent or self.env
            base_domain = os.path.basename(global_env.path)
            dns_value = base_domain \
                        if not self.dns_value and self.dns_type == 'CNAME' \
                        else self.dns_value
            if dns_value:
                subdom = resource.prefix
                try:
                    self._dns_add(self.dns_type, subdom, base_domain, dns_value)
                except:
                    self.log.exception("[DNS] Registration error for %s",
                                       subdom)
                else:
                    self.log.info('[DNS] Domain %s registered successfully',
                                  subdom)
            else:
                self.warning('[DNS] Invalid config: DNS target is empty')

    def resource_changed(self, resource, old_values, context):
        """Do nothing"""

    def resource_deleted(self, resource, context):
        """Do nothing"""

    def resource_version_deleted(self, resource, context):
        """Do nothing"""

    # Internal methods

    def _dns_add(self, dns_type, subdom, base_domain, dns_value, ttl=14400):
        """Add DNS record for product (sub)domain
        """
        import dns.query
        import dns.tsigkeyring
        import dns.update
        keyring = dns.tsigkeyring.from_text({self.tsig_keyname : self.tsig_key})
        update = dns.update.Update(subdom, keyring=keyring)
        update.add(subdom, ttl, dns_type, base_domain + '.')
        response =  dns.query.tcp(update, self.dns_server_host)
        # TODO: Analyze response contents. What if it represents a failure ?


# Two-level product path namespace
# https://issues.apache.org/bloodhound/wiki/Proposals/BEP-0003#deploy-sibling-paths

def helper_bootstrap_siblings(b=None, base_path=None, globalname=u'global',
                              failnomatch=True):
    """Product namespace immediately after environment name

    :param b:          Optional instance of `ProductRoutesBootstrapHandler`.
                       This parameter serves to the purpose of applying product
                       path routes after connecting an initial set of routes
    :param base_path:  Optional path prefix to Bloodhound URL namespace
    :param globalname: Optional string value to reserve an entry for
                       global environment scope. defaults to `'global'`
    :param failnomatch: Setup routes to send an HTTP error back to the client
                       if no match could be made for input URL path.
    """
    b = b or ProductRoutesBootstrapHandler()
    base_path = base_path or u''
    b.mapper.connect(None, u'%s/{envname}/%s/{path_info:.*}' % 
                     (base_path, globalname), action='dispatch')
    b.mapper.connect(None, u'%s/{envname}/{product}/{path_info:.*}' % 
                     (base_path,), action='dispatch')
    b.mapper.connect(None, base_path or u'/', action='envlist')
    if failnomatch:
        # Fallback to error condition if no match
        err = ProductRoutesBootstrapHandler.DEFAULT_MATCH_ERROR.copy()
        update_error_vars = lambda environ, result : result.update(err) or True
        b.mapper.connect('.*', conditions=dict(function=update_error_vars))
    return b

bootstrap_sibling_products = helper_bootstrap_siblings()


# Embedded product path namespace
# Equivalent to default Apache(TM) Bloodhound factories
# https://issues.apache.org/bloodhound/wiki/Proposals/BEP-0003#deploy-global-env-embed

bootstrap_embedded_products = ProductRoutesBootstrapHandler()
bootstrap_embedded_products.mapper.connect(None, 
        u'/{envname}/products/{product}/{path_info:.*}', action='dispatch')
bootstrap_embedded_products.mapper.connect(None, u'/{envname}/{path_info:.*}',
                                           action='dispatch')
bootstrap_embedded_products.mapper.connect(None, u'/', action='envlist')

