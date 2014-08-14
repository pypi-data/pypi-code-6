import time
from pprint import pprint
import getpass as gp

import XenAPI
from progress.spinner import Spinner

from .utils import abort


def get_creds():
    print "Enter XenServer API credentials:"
    username = raw_input("Username[{}]: ".format(gp.getuser()))
    password = ''
    if username == '':
        username = gp.getuser()
    while password == '':
        password = gp.getpass()
    return username, password


def get_session(poolurl):
    session = None
    username, password = get_creds()
    while session is None:
        print "\nEstablishing session..."
        try:
            session = XenAPI.Session(poolurl)
            session.xenapi.login_with_password(username, password)
        except XenAPI.Failure as ex:
            if ex.details[0] == 'HOST_IS_SLAVE':
                print ("XenServer returned HOST_IS_SLAVE. Redirecting "
                       "to current master [{}]").format(ex.details[1])
                poolurl = "https://{}".format(ex.details[1])
                session = None
            elif ex.details[0] == 'SESSION_AUTHENTICATION_FAILED':
                print "ERROR: Invalid credentials\n"
                username, password = get_creds()
                session = None
            else:
                abort("XenAPI error: {}".format(ex))
        except IOError as ex:
            abort("Invalid URL: {}".format(ex))
    return session


def create_vm(session, params, config):
    """
    Creates a new vm from XenServer template.
    """
    print "\nEngage.\n"

    # Find uuid's on server
    template_ref = session.xenapi.VM.get_by_uuid(params['template'][1])
    network_ref = session.xenapi.network.get_by_uuid(params['network'][1])

    clone_task = session.xenapi.Async.VM.clone(template_ref, params['hostname'])
    spinner = Spinner("Cloning template... ")
    while session.xenapi.task.get_status(clone_task) == 'pending':
        spinner.next()
        time.sleep(1)
    spinner.finish()

    clone_task_record = session.xenapi.task.get_record(clone_task)
    if clone_task_record['status'] == 'success':
        print "\nTemplate cloned."
        vm_ref = session.xenapi.task.get_result(clone_task)
        # Need to slice because result comes wrapped in tag
        vm_ref = vm_ref[7:-8]
    else:
        pprint(clone_task_record)
        abort("Couldn't clone VM.")
    session.xenapi.task.destroy(clone_task)

    # VIF params
    # There should be no device in slot 0
    vif = {
        'device': '0',
        'network': network_ref,
        'VM': vm_ref,
        'MAC': "",
        'MTU': "1500",
        'qos_algorithm_type': "",
        'qos_algorithm_params': {},
        'other_config': {}
    }

    # Network, disk, boot arguments
    try:
        session.xenapi.VIF.create(vif)
        session.xenapi.VM.provision(vm_ref)

        # append MCHM url to template bootargs
        if config['mchm_enable']:
            boot_args = session.xenapi.VM.get_PV_args(vm_ref)
            boot_args = '{} url={}'.format(boot_args, params['mchm_vm_url'])
            session.xenapi.VM.set_PV_args(vm_ref, boot_args)

    except XenAPI.Failure as ex:
        abort("Error provisioning VM: XenAPI failure {}".format(ex.message))

    # Engage.
    spinner = Spinner("Starting VM... ")
    start_task = session.xenapi.Async.VM.start(vm_ref, False, True)
    while session.xenapi.task.get_status(start_task) == 'pending':
        spinner.next()
        time.sleep(1)
    spinner.finish()

    start_task_record = session.xenapi.task.get_record(start_task)
    session.xenapi.task.destroy(start_task)

    if start_task_record['status'] == 'success':
        print "\nVM started."
    else:
        pprint(start_task_record)
        abort("Couldn't start VM.")
