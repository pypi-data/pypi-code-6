import os
import shutil
import urllib2
from urlparse import urljoin
from xl_helper.FileUtils import FileUtils
from subprocess import Popen, PIPE, STDOUT
from xl_helper.Utils import Utils


class Server:

    @staticmethod
    def from_config(config, home):
        return Server(
            home=home,
            username=config.get('deployit', 'username'),
            password=config.get('deployit', 'password'),
            url="{protocol}://{host}:{port}/deployit/".format(
                protocol=config.get('deployit', 'protocol'),
                host=config.get('deployit', 'host'),
                port=config.get('deployit', 'port')
            )
        )

    def __init__(self, home, username, password, url):
        self.home = home
        self.username = username
        self.password = password
        self.url = url + '/' if url[-1] != '/' else url

    def is_stopped(self):
        return not self._ping()

    def is_running(self):
        return self._ping()

    def restart(self):
        self.stop()
        self.start()

    def start(self):
        if self.is_stopped():
            server_sh_file = "{}/bin/server.sh".format(self.home)

            if not os.path.isdir("{path}/repository".format(path=self.home)):
                print "Initializing XL Deploy with default configuration."
                config_path = FileUtils.to_absolute_path("xl_helper/resources/deployit.conf")
                print "It is taken from %s " % config_path
                shutil.copy(config_path, os.path.join(self.home, "conf"))
                p = Popen([server_sh_file, '-setup', '-reinitialize'], bufsize=0, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
                p.stdin.write("yes\n")
                p.stdin.flush()
                p.communicate()

            if not os.path.isfile(server_sh_file):
                print "Server cannot be started as file {} hasn't been found".format(server_sh_file)
            else:
                os.system(server_sh_file)
        else:
            print "Server is already started"

    def stop(self):
        if self.is_running():
            stop_url = self.url + 'server/shutdown'
            opener = Utils.auth_and_open_url(stop_url, 'POST', self.username, self.password)
            print "Stopping the server"
            urllib2.install_opener(opener)

    def _ping(self):
        try:
            ping_url = self.url + 'server/info'
            print "Pinging %s " % ping_url
            opener = Utils.auth_and_open_url(ping_url, 'GET', self.username, self.password)
            urllib2.install_opener(opener)
            return True
        except urllib2.URLError:
            return False
