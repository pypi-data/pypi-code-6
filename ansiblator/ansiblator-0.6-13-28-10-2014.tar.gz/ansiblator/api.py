# !/usr/bin/env python
# -*- coding:utf-8 -*-

# (c)Ing. Zdenek Dlauhy, Michal Dlauhý, info@pripravto.cz, www.pripravto.cz


import subprocess
import os
import functools

# TODO: fix logging and messages
# import logging
# logging.basicConfig(level=logging.DEBUG)
# log = logging.getLogger("ans wrapper")

class log(object):

    @staticmethod
    def info(msg):
        print(msg)

    @staticmethod
    def debug(msg):
        pass
    warn = info
    error = info

try:
    import ansible.runner
    import ansible.inventory
    from ansible.utils.plugins import module_finder
except ImportError as e:
    log.error("Cannot import Ansible! Ansiblator will not work. {}".format(e))
    log.error("Run:  pip install ansible")


"""
Main module of Ansiblator - wrapper around Ansible for Python

Classes
-------

Ansiblator() - actuall wrapper
DictToInventory - convertor for inventory files
"""
try:
    from ansiblator.version import __version__
except ImportError:
    __version__ = 0

__version__ = "0.6-{}".format(__version__)
__author__ = "pripravto-service"
__email__ = "test@dlauhy.cz"
__url__ = "http://www.pripravto.cz"
__desc__ = "Ansiblator - makes Ansible api more Pythonic"
__sys_name__ = "ansiblator"
__license__ = "GPLv3"



class DictToInventory(object):
    """

    dict to inventory file mapper::

        import ansiblator.api as an
        dict_data = {'pc':[{'ssh_host':'192.168.0.10', 'ssh_user':'test_user', 'su_user':'root'},
               {'ssh_host':'192.168.0.8', 'ssh_user':'test_user', 'su_user':'root'}],
        'test':[{'ssh_host':'example.cz', 'ssh_user':'test_user2', 'su_user':'root', 'su_pass':'pass'}]}
        inv = an.DictToInventory(dict_data, filename="/tmp/out")
        inv = ansible.inventory.Inventory("/tmp/out")
        inv.get_hosts("example.cz")[0].vars

    """
    def __init__(self, dict_data, filename="/tmp/out"):
        """
        :param dict_data: dict which would be converted to inventory
        :type dict_data: dict
        :param filename: filanema
        :type filename: str
        """
        self.data = []
        self.filename = filename
        self.dict_to_inverntory(dict_data)
        self.data_to_text()
        log.info("Dictionary converted to ansible host file {}".format(filename))

    def dict_to_inverntory(self, dict_data):
        """convert dict data into inventory file"""
        for group, variables in dict_data.items():
            self.data.append("[{}]".format(group))
            for host_vars in variables:
                self.data.append(self.host_into_text(**host_vars))
            self.data.append("\n")

    def host_into_text(self, ssh_host="hostname", ssh_user=None, su_pass=None, su_user=None, sudo_pass=None, **kwargs):
        """transforms parameters into inventory line"""
        data = locals()
        data.update(kwargs)
        del data['kwargs']
        del data['self']
        buff = []
        _buffer = ['ssh_host', 'ssh_user', 'su_pass', 'su_user', 'sudo_pass'] + kwargs.keys()
        for k in _buffer:
            if k in data and data[k] is not None:
                if k == 'ssh_host':
                    buff.append(data[k])
                else:
                    buff.append("ansible_{}={}".format(k, data[k]))
        return " ".join("{}".format(key) for key in buff)

    def data_to_text(self, filename=None):
        """save all data into text"""
        if filename is None:
            filename = self.filename
        with open(filename, "w") as writer:
            for text in self.data:
                writer.write(text)
                writer.write("\n")
            writer.close()


class Ansiblator(object):
    """
    Ansiblator
    ==========

    Ansiblator - makes Ansible api more Pythonic

    This wrapper allows more easier way how to use Ansible in Python.
    Chain commands without without playbooks. More like Fabric.

    With this Ansible can be more powerfull and it will allow to chain commands with
    python commands. Ansible documentation is on http://docs.ansible.com/.
    API is now trying to feel like Fabric, but it's still not complete, there
    will be some changes.

    Get started
    ===========

    For instalation you can download package and then just unpack package from
    https://pypi.python.org/pypi/ansiblator and use it::

        python setup.py install

    or install by pip::

        pip install ansiblator


    Quickstart
    ==========

    For most quickest example you can just create your ansible host file named
    ansible_hosts inside your home directory or give full path to file.

    Ansiblator is mainly using file such as in ~/ansible_hosts.

    code::

        import ansiblator.api as an
        ans = an.Ansiblator()
        ret = ans.local("uname -a", now=True, use_shell=True)
        ans.run("uname -a", now=True)
        ans.runner("uptime")
        ans.run_all()
        ans.copy(src="/tmp/aabc.csv", dest="/tmp/",pattern="pc",now=True)

    specify ansible hosts file and select pattern::

        ans = an.Ansiblator(inventory="/tmp/ansible_file", pattern="pc")

    use dictionary to create inventory::

        inv = {'pc':[{'ssh_host':'192.168.0.10', 'ssh_user':'test_user', 'su_user':'root'},
                    {'ssh_host':'192.168.0.12', 'ssh_user':'test_user2', 'su_pass':'paasswd','su_user':'root'}]}
        ans = an.Ansiblator(inventory=inv)
        ans.run("uname -a", now=True)

    prepare commands and run after::

        ans = an.Ansiblator(run_at_once=False)
        ans.get(src="/tmp/file", dest="/tmp/")
        ans.get(src="/tmp/file2", dest="/tmp/")
        ans.run_all()

    make custom class::

        class Automatization(Ansiblator):

            def update_server(self, su=True,sudo=False):
                self.run("apt-get update", su=su, sudo=sudo)
                self.run("apt-get upgrade -y", su=su, sudo=sudo)

    use custom class and more patterns together::

        ans = Automatization(pattern=['servers', 'production', 'test', 'pc'])
        ans.update_server()

    With this, you can create full commands or functions and just pass to them
    pattern and run at the end.

    Need all modules inside Ansible?::

        ans = an.Ansiblator()
        ans.get_all_modules()
        #now you should be able to do >
        ans.user(name="hugo")
        #or even
        ans.pip(name="six", virtualenv="/tmp/venv", virtualenv_site_packages="yes")


    More information
    ================

    Ansiblator automatically saves returned json values for actuall runs, so
    you can use them for testing and conditions. For example

    testing::

        return_code = ans.local("uname -a", now=True, use_shell=True)
        return_code['contacted']

        or

        return_code = ans.local(["uname", "-a"], now=True, use_shell=False)
        return_code['contacted']

    Todo
    ====

    - make more tests
    - improve logging
    - improve DictToInventory mapper, so more options are possible, such as groups and so on

    Changes
    =======

    - ability to run on more patterns
    - fixes on more runs
    - run all modules on ansible

    Info
    ====

    For more information you can consult functions or actual Ansible documentation.
    More information can be also used on http://www.pripravto.cz. You can also
    contact us there.
    """
    def __init__(self, inventory="ansible_hosts", pattern="all",
                 module_name="command", run_at_once=False, sudo=False, su=False,
                 su_user=None, host=None, stop_on_error=True, use_shell=True):
        """
        :param inventory: string or dict, which defines inventory
        :type inventory: str or dict
        :param pattern: pattern maching
        :type pattern: str
        :param module_name: ansible module
        :type module_name: str
        :param run_at_once: run commands when issued or wait
        :type run_at_once: bool
        :param sudo: run as sudo
        :type sudo: bool
        :param su: run as su
        :type su: bool
        :param su_user: specify su user
        :type su_user: str
        :param host: specify host
        :type host: list
        :param stop_on_error: stop exection on return error
        :type stop_on_error: bool
        :param use_shell: use shell on subprocess
        :type use_shell: bool
        """
        self.pattern = pattern
        self.module_name = module_name
        self.runners = []
        self.ret_codes = []
        self.run_at_once = run_at_once
        self.sudo = sudo
        self.su = su
        self.su_user = su_user
        self.host = host
        self.stop_on_error = stop_on_error
        self.use_shell = use_shell
        self.inventory = self.parse_inventory(inventory)
        log.info("Intializing ansible: {}".format(self))

    def get_host_var(self, host):
        return self.inventory.get_variables(host)

    def get_all_modules(self):
        """list all modules and attach them to Ansbilator"""
        # constant and code copied from ansible
        # https://github.com/ansible/ansible/blob/devel/bin/ansible-doc
        BLACKLIST_EXTS = ('.swp', '.bak', '~', '.rpm')
        paths = (p for p in module_finder._get_paths() if os.path.isdir(p))
        modules = []
        for path in paths:
            modules.extend(m for m in os.listdir(path) if m not in BLACKLIST_EXTS)
        for module_name in modules:
            self.attach_module(module_name)

    def attach_module(self, module_name):
        """Attach module to Ansiblator"""
        if hasattr(self, module_name):
            log.warn('Cannot attach module {}'.format(module_name))
            return None
        func = functools.partial(self.run, cmd=None, module_name=module_name, use_ansible=True)
        setattr(self, module_name, func)

    def parse_inventory(self, inventory, new_filename="ansible_dict_convert"):
        """
        :param inventory: some inventory specification
        :type inventory: dict or str
        :param new_filename: if you pass dict to inverntory, you can name it
        :type new_filename: str
        """
        log.info("Parsing inventory object {}".format(inventory))
        home = os.environ.get('HOME', '/tmp/')
        if isinstance(inventory, str):
            if not inventory.startswith("/"):
                filename = "{}/{}".format(home, inventory)
            else:
                filename = "{}".format(inventory)
        elif isinstance(inventory, dict):
            filename = "{}/{}".format(home, new_filename)
            DictToInventory(inventory, filename=filename)
        else:
            pass
        if isinstance(inventory, ansible.inventory.Inventory):
            pass
        else:
            inventory = ansible.inventory.Inventory(filename)
        return inventory


    def get_group_host(self, group):
        host_list = self.inventory.get_group(group).hosts
        data = None
        for host in host_list:
            if "ansible_su_pass" in host.vars or "ansible_sudo_pass" in host.vars:
                data = host.vars
                break
        return data

    def get_host_vars(self, data, su=None, sudo=None, su_pass=None,
                      sudo_pass=None, su_user=None):
        """get data values from data"""
        if data:
            if su:
                su_pass = data.get("ansible_su_pass", su_pass)
                su_user = data.get("ansible_su_user", su_user)
            if sudo:
                sudo_pass = data.get("ansible_sudo_pass", sudo_pass)
            return su_pass, sudo_pass, su_user
        else:
            return None, None, None

    def create_argument(self, cmd, kwargs):
        """
        :param cmd: command to run
        :type cmd: str
        :param kwargs: optional arguments
        :type kwargs: dict
        """
        args = " ".join("{}={}".format(k, v) for k, v in kwargs.items())
        if args == " ":
            args = ""
        if cmd is None:
            cmd = "{}".format(args)
        else:
            if args == "":
                cmd = "{}".format(cmd)
            else:
                cmd = "{} {}".format(cmd, args)
        return cmd

    def runner_ans(self, cmd="uptime", pattern=None, module_name=None, inventory=None,
                   now=None, su=None, sudo=None, su_user=None, su_pass=None,
                   sudo_pass=None, host=None, **kwargs):
        """main ansible wrapper"""
        if module_name is None:
            module_name = self.module_name
        if pattern is None:
            pattern = self.pattern
        if not isinstance(pattern, list):
            pattern = [pattern]
        if inventory is None:
            inventory = self.inventory
        else:
            inventory = self.parse_inventory(inventory)
        if now is None:
            now = self.run_at_once
        if sudo is None:
            sudo = self.sudo
        if su is None:
            su = self.su
        if su_user is None:
            su_user = self.su_user

        if host is None:
            host = self.host
        if host is None:
            for pat in pattern:
                data = self.get_group_host(pat)
                host_list = None
                info = dict(locals())
                del info['self']
                self._run(self._runner_ans(**info), now)
        else:
            host_list = [host]
            pattern = None
            data = self.get_host_var(host)
            info = dict(locals())
            del info['self']
            self._run(self._runner_ans(**info), now)

    def _runner_ans(self, data=None, cmd=None, pattern=None, module_name=None, inventory=None,
                   now=None, su=None, sudo=None, su_user=None, su_pass=None,
                   sudo_pass=None, host_list=None, host=None, pat=None, **kwargs):
        su_pass, sudo_pass, su_user = self.get_host_vars(data, su, sudo, su_pass, sudo_pass, su_user)
        info = dict(locals())
        del info['data']  # remove to skip output of password out to shell
        del info['su_pass']
        del info['sudo_pass']
        del info['pattern']  # running pat instead of pattern - FOR CYCLE UP
        log.debug(info)
        cmd = self.create_argument(cmd, kwargs.get('kwargs', {}))
        log.info("Creating new command '{}' on '{}'".format(cmd, module_name))
        runner = ansible.runner.Runner(pattern=pat, host_list=host_list,
                                       module_name=module_name, su_pass=su_pass,
                                       module_args=cmd, inventory=inventory,
                                       su=su, sudo=sudo, su_user=su_user,
                                       sudo_pass=sudo_pass)
        return runner


    def runner_local(self, cmd="uptime", module_name=None, now=None, use_shell=None, **kwargs):
        """
        :param cmd: command to run
        :type cmd: str
        :param module_name: module name -
        :type module_name:
        :param now: when to run command
        :type now: bool
        """
        if now is None:
            now = self.run_at_once
        runner = {'cmd':cmd, 'module_name':module_name}
        return self._run(runner, now, use_shell)

    def _run(self, runner, now=None, use_shell=None):
        """
        :param runner: runner object to run
        :type runner: dict or obj
        :param now: run now?
        :type now: bool
        :param use_shell: use shell when subbprocess is running
        :type use_shell: bool

        function to run or append runner
        """
        if now is None:
            now = self.run_at_once
        if use_shell is None:
            use_shell = self.use_shell
        if now:
            log.info("Running {}".format(runner))
            if isinstance(runner, dict):
                ret_code = self._runner_local(runner, use_shell)
            else:
                ret_code = runner.run()
            self.parse_ret_code(ret_code)
            self.ret_codes.append(ret_code)
            log.info(ret_code)
            return ret_code
        else:
            self.runners.append(runner)
            return {"run":False}

    def _runner_local(self, runner, use_shell):
        """low level local runner"""
        try:
            ret_code = subprocess.Popen(runner['cmd'], stdout=subprocess.PIPE, shell=use_shell)
            out, err = ret_code.communicate()
            return_c = ret_code.returncode
        except OSError as e:
            log.error(e)
            return_c = 1
            out = None
            err = e
        if return_c == 0:
            failed = False
        else:
            failed = True
        return {'contacted':{'local':{'stdout':out, 'failed':failed ,
                                      'stderr':err, 'ret_code':return_c}}, 'dark':{}}


    def runner(self, cmd="uptime", use_ansible=True, module_name="command",
               inventory=None, now=None, pattern=None, **kwargs):
        """
        :param cmd: command to run
        :type cmd: str
        :param use_ansible: do you want to use ansible or local subprocess?
        :type use_ansible: bool
        :param module_name: name of ansible module
        :type module_name: str
        :param inventory: inventory object
        :type inventory: <inventory>
        :param now: should this run be imideatly created?
        :type now: bool
        :param pattern: pattern matching on machines
        :type pattern: str

        main runner method which acts as medium to other calls
        """
        log.info("Making new runner: {}".format(cmd))
        if use_ansible:
            return self.runner_ans(cmd=cmd, module_name=module_name,
                                   inventory=inventory, now=now, pattern=pattern,
                                   **kwargs)
        else:
            return self.runner_local(cmd=cmd, module_name=module_name,
                                     inventory=inventory, now=now, pattern=pattern,
                                     ** kwargs)

    run = runner

    def copy(self, cmd=None, module_name="copy", src="", dest="", **kwargs):
        return self.runner(cmd=cmd, use_ansible=True, module_name=module_name,
                           src=src, dest=dest, **kwargs)
    put = copy

    def fetch(self, cmd=None, module_name="fetch", src="", dest="", **kwargs):
        return self.runner(cmd=cmd, use_ansible=True, module_name=module_name,
                           src=src, dest=dest, **kwargs)
    get = fetch

    def ping(self, cmd=None, module_name="ping", **kwargs):
        return self.runner(cmd=cmd, use_ansible=True, module_name=module_name,
                           **kwargs)

    def local(self, cmd=None, **kwargs):
        return self.runner(cmd=cmd, use_ansible=False, **kwargs)
    run_cmd = local

    def run_all(self, now=True):
        """run all runners inside class"""
        for runner in self.runners:
            self._run(runner, now)

    def parse_ret_errors(self, code):
        """quick check if stop_on_error is active"""
        if self.stop_on_error:
            for k, v in code['contacted'].items():
                # log.info(v) # assuming, that run was mostly succesfull
                if v.get('failed', False):
                    raise Exception("ERROR: run was not successfull {}".format(v))

    def parse_ret_code(self, code):
        """parse return code"""
        self.parse_ret_errors(code)
        log.info("Contacted servers :")
        log.info("\n".join("{}: {}".format(k, v.get('stdout', v.get('msg', None))) for k, v in code['contacted'].items()))
        log.warn("Error in contacting :")
        log.info("\n".join("{}: {}".format(k, v.get('msg', None)) for k, v in code['dark'].items()))
        pass


__description__ = Ansiblator.__doc__

if __name__ == "__main__":
    ans = Ansiblator(pattern="test", stop_on_error=False, run_at_once=True)
    ans.get_all_modules()
    ans.copy(src="/tmp/aaa.csv", dest="/tmp/aaa/")
    ans.user(name="ds")
    def second_test(ans):
        ans.local(["uname", "-a"], now=True)
        ans.local("uname -a", now=True)
        ret = ans.local("uname -a", now=True, use_shell=True)
        if ret['contacted']:
            for k, v in ret['contacted'].items():
                print(k, v.get('stdout', None), v.get("stderr", None))
        ans.run("uptime")
        ans.run_at_once = False
        ans.run("touch /tmp/aaa.csv")
        ans.local(["uname", "-a"])
        ans.get(src="/tmp/aaa.csv", dest="/tmp/")
        ans.run_all()

    second_test(ans)


