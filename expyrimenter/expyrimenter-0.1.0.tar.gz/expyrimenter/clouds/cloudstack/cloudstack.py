from .api import API
from .statemonitor import StateMonitorProcess
from expyrimenter import Executor, SSH
from time import sleep
from urllib.error import HTTPError
import threading
import logging


class CloudStack:
    _id_cache = None

    def __init__(s, executor=None, api=None):
        if executor is None:
            executor = Executor()
        if api is None:
            api = API()

        s.executor = executor
        s._api = api
        s._logger = logging.getLogger('cloudstack')

        s._sm_lock = threading.Lock()
        s._sm_users = 0

    def get_states(s):
        vms = s._api.listVirtualMachines()['virtualmachine']
        return {vm['name']: vm['state'] for vm in vms}

    def get_id(s, name):
        cache = CloudStack._id_cache
        if cache is None or not name in cache:
            s.load_id_cache()

        return CloudStack._id_cache[name]

    def get_state(s, name):
        vm_id = s.get_id(name)
        vms = s._api.listVirtualMachines(id=vm_id)['virtualmachine']
        return vms[0]['state']

    def start(s, *names):
        names = s._ensure_lists(names)
        for name in names:
            s._logger.info('Starting %s' % name)
            vm_id = s.get_id(name)
            s._submit_sm_user(start_vm, 'start VM', name, vm_id)

    def stop(s, *names):
        names = s._ensure_lists(names)
        for name in names:
            vm_id = s.get_id(name)
            s.executor.run_fn(stop_vm, 'stop VM', name, vm_id)

    def get_deploy_params(s, name):
        vm_id = s.get_id(name)
        vm = s._api.listVirtualMachines(id=vm_id)['virtualmachine'][0]
        keys = ['serviceofferingid', 'templateid', 'zoneid']

        params = {}
        for key in keys:
            params[key] = vm[key]

        return params

    def deploy(s, params, **kwargs):
        if kwargs:
            params.update(kwargs)
        future = s._submit_sm_user(deploy_vm, 'deploy VM', params)

    def deploy_like(s, existent, new, **kwargs):
        params = s.get_deploy_params(existent)
        params['name'] = new
        s.deploy(params, **kwargs)

    def load_id_cache(s):
        vms = s._api.listVirtualMachines()['virtualmachine']
        CloudStack._id_cache = {vm['name']: vm['id'] for vm in vms}
        return CloudStack._id_cache

    def _submit_sm_user(s, fn, title, *args, **kwargs):
        with s._sm_lock:
            s._sm_users += 1
            StateMonitorProcess.start()

        states = StateMonitorProcess.get_states()
        args += (states,)
        future = s.executor.run_fn(fn, title, *args, **kwargs)
        future.add_done_callback(s._sm_user_done)

        return future

    def _sm_user_done(s, future):
        with s._sm_lock:
            s._sm_users -= 1
            if s._sm_users == 0:
                StateMonitorProcess.stop()

    def _ensure_lists(s, args):
        lists = []
        for arg in args:
            if isinstance(arg, list):
                lists += arg
            else:
                lists.append(arg)
        return lists


def stop_vm(name, vm_id):
    api = API()
    result = api.stopVirtualMachine(id=vm_id)
    msg = 'Sent %s stop request.' % name
    logging.getLogger('cloudstack').debug(msg)


def start_vm(name, vm_id, states):
    api = API()
    api.startVirtualMachine(id=vm_id)
    wait_ssh(name, states)
    msg = '%s is up.' % name
    logging.getLogger('cloudstack').info(msg)


def deploy_vm(params, states):
    api = API()
    api.deployVirtualMachine(**params)
    log = logging.getLogger('cloudstack')
    if 'startvm' in params and params['startvm'] is False:
        msg = '%s is deployed.' % params['name']
        log.debug(msg)
    else:
        wait_ssh(params['name'], states)
        msg = '%s is ready for SSH.' % params['name']
        log.info(msg)


def wait_ssh(name, states):
    wait_state(name, 'Running', states)
    SSH.await_availability(name)


def wait_state(name, state, states, interval=5):
    while True:
        if state == states.get(name):
            break
        sleep(interval)
