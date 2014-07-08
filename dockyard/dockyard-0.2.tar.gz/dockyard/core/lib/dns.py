import json
import docker
import sys, os
import subprocess
import re

def run(cmd, returncode=False, echo=True, **kargs):
    """ Executes a shell command and prints out STDOUT / STDERROR, exits on failure by default """
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, **kargs)
    if echo:
        print "$ %s" % cmd
    
    while True:
        out = process.stdout.read(1)
        if out == '' and process.poll() != None:
            break
        if out != '':
            sys.stdout.write(out)
            sys.stdout.flush()

    if returncode:
        return process.returncode
    else:
        if process.returncode != 0:
            print "Something went wrong! returncode=%s" % process.returncode
            sys.exit(1)


class Dns(object):

    configFile = 'dockyard.json'
    dnsTemplateFile = 'lib/dns.tpl' 
    zoneFilename = 'named.conf.default-zones'
    dockerClient = None

    def __init__(self, dockerClient=None):
        self.dockerClient = dockerClient

    def configure(self, dockyardName):

        dockyardConfig = json.load(open(self.configFile))
        domainName = dockyardConfig['dockyards'][dockyardName]['domain']

        activeContainers = []
        for containerInfo in self.dockerClient.containers():
            inspectInfo = self.dockerClient.inspect_container(containerInfo['Id'])
            activeContainers.append({ 'name': containerInfo['Image'].split(':')[0] , 'ip': inspectInfo['NetworkSettings']['IPAddress'] })


        content = open(self.dnsTemplateFile).read()

        # Compile list of A entries
        aEntries = ''
        for container in activeContainers:
            aEntries = aEntries + '%(name)s   IN  A   %(ip)s\n' % container

        replace = {'hostname': dockyardConfig['dockyards'][dockyardName]['domain'], 'aEntries': aEntries}

        f = open('temp/' + domainName,'w')
        f.write(content % replace)
        f.close()

        # Copy new zone file from vagrant share into dns config direction + fix permissions
        run('vagrant ssh --command "sudo cp /vagrant/temp/%s /etc/bind/%s"' % (domainName, domainName))
        run('vagrant ssh --command "sudo chown bind:bind /etc/bind/%s"' % (domainName))
        
        # Copy DNS configuration to Vagrant share so we can operate on it from host machine
        run('vagrant ssh --command "cp /etc/bind/%s /vagrant/temp/%s"' % (self.zoneFilename, self.zoneFilename))
        zoneContents = open('temp/' + self.zoneFilename).read()

        # Check to see if we have the zone included
        match = re.search(domainName, zoneContents, re.IGNORECASE)
        if not match:
            zoneContents = zoneContents + 'zone "%s" { type master; file "/etc/bind/%s"; };\n' % (domainName, domainName)
            f = open('temp/' + self.zoneFilename,'w')
            f.write(zoneContents)
            f.close()

            # Copy from Vagrant share back to /etc/
            run('vagrant ssh --command "sudo cp /vagrant/temp/%s /etc/bind/%s"' % (self.zoneFilename, self.zoneFilename))
            run('vagrant ssh --command "sudo chown bind:bind /etc/bind/%s"' % (self.zoneFilename))

        # Reload DNS entries
        run('vagrant ssh --command "sudo service bind9 reload"')

