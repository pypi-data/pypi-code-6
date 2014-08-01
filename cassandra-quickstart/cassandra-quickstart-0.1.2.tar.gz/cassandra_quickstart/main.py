import os
import sys
import shutil
import subprocess
import csv
import shlex
import platform

import argparse
import virtualenv

from cassandra_quickstart import config
from cassandra_quickstart.util import download, makedirs
from cassandra_quickstart.java import setup_java

cqs_home = os.path.expanduser("~/.cassandra-quickstart")
virtualenv_path = os.path.join(cqs_home, "virtualenv")
ccm_home = os.path.join(cqs_home, "ccm")

def create_virtualenv():
    """Create a virtualenv in ~/.cassandra-quickstart/virtualenv"""
    if os.path.exists(virtualenv_path):
        shutil.rmtree(virtualenv_path)
    virtualenv.create_environment(virtualenv_path)
    
    # Install dependencies:
    def pip_install(module):
        script = "import pip\npip.main(['install','{module}'])".format(module=module)
        p = subprocess.Popen([os.path.join(virtualenv_path, 'bin', 'python'), '-c', script], 
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print(p.communicate()[0])
        
    # Install a version of ccm that understands stable, oldstable tags.
    # This won't be necessary once
    # https://github.com/pcmanus/ccm/pull/137 is merged.
    print("Installing python dependencies into virtualenv ...")
    pip_install('https://github.com/EnigmaCurry/ccm/archive/version-tags.zip')

def activate_virtualenv():
    """Activate the virtualenv.  This isn't as good as 'source
    bin/activate' because we still have all the original sys.path
    entries, but the virtual ones are at least listed first."""
    
    activate_script = os.path.join(virtualenv_path, 'bin', 'activate_this.py')
    if not os.path.exists(activate_script):
        create_virtualenv()
    with open(activate_script) as f:
        exec(f.read(), dict(__file__=activate_script))

    # Import the virtualenv libraries:
    global ccmlib, yaml
    import ccmlib, ccmlib.cluster, ccmlib.cmds, ccmlib.cmds.command, ccmlib.cmds.cluster_cmds, ccmlib.cmds.node_cmds
    import yaml

def is_cassandra_running():

    def windows_get_cassandra_procs():
        p = subprocess.Popen(shlex.split('wmic process where "name=\'java.exe\'" get Commandline,Name,Processid /format:csv'), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        reader = csv.reader(iter(p.stdout.readline, ''))
        for row in reader:
            if len(row) >= 4 \
               and row[2] == 'java.exe' \
               and "org.apache.cassandra.service.CassandraDaemon" in row[1]:
                return True
        return False

    def unix_get_cassandra_procs():
        system = platform.system().lower()
        if 'linux' in system:
            cmd = 'ps xw -o comm,args'
        else:
            # Assume MacOS or bsd like:
            cmd = 'ps -cexww -o comm,args'
        p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in iter(p.stdout.readline, ''):
            if line.startswith('java') and 'org.apache.cassandra.service.CassandraDaemon' in line:
                return True
        return False

    system = platform.system().lower()
    if system in ['windows','win32']:
        return windows_get_cassandra_procs()
    else:
        return unix_get_cassandra_procs()
    
def is_cassandra_installed(cluster_name='cassandra'):
    cluster_path = os.path.join(ccm_home, cluster_name)
    if not os.path.exists(cluster_path):
        print("Cassandra is not installed yet. You must run 'cqs install' first.")
        return False
    return True

def install(version='stable', cluster_name='cassandra', **kwargs):
    """Install cassandra via ccm"""
    java_home = setup_java()
    cluster_path = os.path.join(ccm_home, cluster_name)

    if os.path.exists(cluster_path):
        print("Cassandra cluster already created at {cluster_path}".format(**locals()))
        return

    if is_cassandra_running():
        print("Another Cassandra process is already running. You must stop it (cqs stop --force) before you can install Cassandra with this tool.")
        return

    makedirs(ccm_home)    

    try:
        cluster = ccmlib.cluster.Cluster(ccm_home, cluster_name, cassandra_version=version, verbose=True)
        with open(os.path.join(cluster_path, 'cassandra.in.sh'), 'w') as f:
            f.write("JAVA_HOME={java_home}\n".format(**locals()))
        cluster.populate(1)
        start(cluster_name=cluster_name)
    except:
        # If any problem occurs, clean things up by destroying the cluster:
        destroy(cluster_name)
        raise

    print("Cassandra started.")

def destroy(cluster_name='cassandra', **kwargs):
    if is_cassandra_installed():
        cluster = ccmlib.cluster.Cluster.load(ccm_home, cluster_name)
        cluster.remove()

def cqlsh(cluster_name='cassandra', **kwargs):
    if is_cassandra_installed():
        cluster = ccmlib.cluster.Cluster.load(ccm_home, cluster_name)
        cmd = "{cqlsh} 127.0.0.1 {args}".format(
            cqlsh=os.path.join(cluster.get_cassandra_dir(), 'bin', 'cqlsh'),
            args=''.join(kwargs['args']))
        os.system(cmd)

def nodetool(cluster_name='cassandra', **kwargs):
    if is_cassandra_installed():
        cluster = ccmlib.cluster.Cluster.load(ccm_home, cluster_name)
        cmd = "{nodetool} -p 7100 {args}".format(
            nodetool=os.path.join(cluster.get_cassandra_dir(), 'bin', 'nodetool'),
            args=''.join(kwargs['args']))
        os.environ['CASSANDRA_INCLUDE'] = os.path.join(ccm_home, cluster_name, 'node1', 'bin', 'cassandra.in.sh')
        os.system(cmd)
        
def stop(cluster_name='cassandra', **kwargs):
    if is_cassandra_installed():
        cluster = ccmlib.cluster.Cluster.load(ccm_home, cluster_name)
        cluster.stop()
        if is_cassandra_running():
            print("Cassandra was told to shut down, but it's still running. You may need to kill it yourself.")

def start(cluster_name='cassandra', **kwargs):
    if is_cassandra_installed():
        if is_cassandra_running():
            print("Cassandra is already running. Use 'cqs stop' to stop it.")
            return
        cluster = ccmlib.cluster.Cluster.load(ccm_home, cluster_name)
        cluster.start()

def info(cluster_name='cassandra', **kwargs):
    """Print info about the installed cluster"""
    pass

def main():
    parser = argparse.ArgumentParser(description='Cassandra Quickstart')
    parser.add_argument('--config', default=None, help="Configuration directory (default is ~/.cassandra-quickstart)", dest='config_directory')
    parser.add_argument('--name', default='cassandra', help="Name of the cluster to operate on (default is 'cassandra')", dest='cluster_name')
    subparsers = parser.add_subparsers()
    
    install_parser = subparsers.add_parser('install', help='Install Cassandra')
    install_parser.add_argument('-v','--version', default='binary:stable')
    install_parser.set_defaults(func=install)

    destroy_parser = subparsers.add_parser('destroy', help='Remove Cassandra')
    destroy_parser.set_defaults(func=destroy)

    start_parser = subparsers.add_parser('start', help='Start Cassandra')
    start_parser.set_defaults(func=start)

    stop_parser = subparsers.add_parser('stop', help='Stop Cassandra')
    stop_parser.add_argument('--force', help='Forcefully terminate Cassandra', action='store_true')
    stop_parser.set_defaults(func=stop)

    cqlsh_parser = subparsers.add_parser('cqlsh', help='Cassandra Shell')
    cqlsh_parser.add_argument('args', nargs=argparse.REMAINDER)
    cqlsh_parser.set_defaults(func=cqlsh)

    nodetool_parser = subparsers.add_parser('nodetool', help='Cassandra node management tool (ex: nodetool ring)')
    nodetool_parser.add_argument('args', nargs=argparse.REMAINDER)
    nodetool_parser.set_defaults(func=nodetool)

    status_parser = subparsers.add_parser('status', help='Print status of cluster')
    status_parser.set_defaults(func=nodetool, args='status')

    help_parser = subparsers.add_parser('help')
    help_parser.set_defaults(func=parser.print_help)

    if len(sys.argv) <= 1:
        parser.print_help()
        exit()
    args = parser.parse_args()
    if args.func == parser.print_help:
        parser.print_help()
    else:
        if args.config_directory is not None:
            global cqs_home, virtualenv_path, ccm_home
            cqs_home = os.path.abspath(os.path.expanduser(args.config_directory))
            virtualenv_path = os.path.join(cqs_home, "virtualenv")
            ccm_home = os.path.join(cqs_home, "ccm")
        activate_virtualenv()
        args.func(**vars(args))

if __name__ == "__main__":
    main()

