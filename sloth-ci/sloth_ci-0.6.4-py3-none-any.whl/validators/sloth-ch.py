def parse_repo_url(repo_url):
    """Extract provider, username, and repo name from the repo URL.
    
    :param repo_url: repo URL, i.e. https://bitbucket.org/moigagoo/sloth-ci

    :returns: provider and repo identifier in form `username/repo`, i.e. 'bitbucket', 'moigagoo/sloth-ci'
    """

    return 'bitbucket', 'moigagoo/sloth-ci'


def get_config_params(request_params):
    """Extract necessary params for Sloth app config creation.
    
    :param request_params: incoming HTTP request params 
    
    :returns: dictionary of all necessary config values
    """

    from slugify import slugify

    title = slugify(request_params.get('title')).lower()
    
    provider, repo = parse_repo_url(request_params.get('repo_url'))
    
    actions = request_params.get('actions') 

    if not (title and provider and repo and actions):
        raise Exception('Some data is missing.')
    
    params = {}

    params['title'] = title
    params['provider'] = provider
    params['repo'] = repo
    params['actions'] = '/n'.join(actions)

    return params


def validate(request, validation_data):
    """Validate params from the Sloth CH front-end and extract necessary data for a Sloth app creation.

    :param request_params: payload to validate
    :param validation_data: dictionary with the key `secret`

    :returns: (True, success message, extracted data dict) if the payload is valid, (False, error message, extracted data dict) otherwise
    """

    from json import loads

    if request.method != 'POST':
        return (False, 'Payload validation failed: Wrong method, POST expected, got {method}.', {'method': request.method})

    trusted_ips = ['188.226.193.156']

    remote_ip = request.headers['Remote-Addr']

    #if remote_ip not in trusted_ips:
    #    return (False, 'Payload validation failed: Unverified remote IP: {ip}.', {'ip': remote_ip})

    try:
        config_params = get_config_params(request.params)

        return (True, 'Payload validated', config_params)

    except Exception as e:
        return (False, 'Payload validation failed: %s' % e, {})
