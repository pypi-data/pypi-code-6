import time
import textwrap

from progress.spinner import Spinner

from .xenserver import create_vm
from .utils import review_choices, hipchat_notification
from .mchm import mchm_render, mchm_upload, mchm_poll
from .puppet import puppet_signcsr


def engage(config, session, params):
    """
    Main control method
    """

    # start time
    start_time = time.time()

    if config['mchm_enable']:
        # Create initial MCHM entry
        mchm_resp = mchm_upload(config['mchm_url'], None, None, iid=None)
        params['mchm_id'] = mchm_resp['id']
        if config['mchm_use_zeroconf']:
            params['mchm_vm_url'] = mchm_resp['zeroconf_url']
        else:
            params['mchm_vm_url'] = mchm_resp['ipv4_url']

        # Generate userdata. Templates have access to everything in the
        # config and params dicts
        userdata, metadata = mchm_render(
            config['mchm_templatedir'], dict(config.items() + params.items()))

        # Upload
        mchm_upload(config['mchm_url'], userdata, metadata,
                    iid=params['mchm_id'])

    # review choices, then use XenAPI to create VM
    review_choices(params, config)
    create_vm(session, params, config)

    # If we're using MCHM, wait for a phonehome
    if config['mchm_enable']:
        mchm_poll(config['mchm_url'], params['mchm_id'],
                  config['mchm_max_polltime'])

    # If Puppet is enabled, attempt to sign node csr
    if config['puppet_enable']:
        timer = 0
        spinner = Spinner("Waiting for cooldown... ")
        while timer < config['puppet_cooldown']:
            time.sleep(1)
            spinner.next()
            timer += 1
        spinner.finish()
        print "\nCooldown expired."
        puppet_signcsr(config, params['fqdn'])

    # Build details string
    vm_addr = 'DHCP'
    if not params['dhcp']:
        vm_addr = params['ip']
    elapsed_time = int(time.time() - start_time)
    if config['mchm_enable']:
        exit_details = "New VM {} ({}) up after {} seconds.".format(
            params['fqdn'], vm_addr, elapsed_time)
    else:
        exit_details = "New VM {} up after {} seconds.".format(
            params['fqdn'], elapsed_time)

    # Hipchat
    if config['hipchat_enable']:
        hc_msg = 'Run complete. {}'.format(exit_details)
        hipchat_notification(config, hc_msg)

    # Print summary and exit
    print "\nRun complete.\n"
    print exit_details
    if config['mchm_enable']:
        print textwrap.dedent("""\
                Generated password: {}

                Smokey The Bear Sez: Remember to change passwords immediately
                if you used the generated password in your templates. This
                password is not necessarily secure, and should be used for
                bootstrapping purposes only.

                Only you can prevent wildfires.\n
                """).format(params['rand_pass'])
    return