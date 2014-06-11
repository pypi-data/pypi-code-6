from mock import MagicMock, call, patch
from mr.awsome import AWS
from unittest2 import TestCase
import os
import pytest
import tempfile
import shutil


class PlainTests(TestCase):
    def setUp(self):
        from mr.awsome.common import import_paramiko
        self.directory = tempfile.mkdtemp()
        self.aws = AWS(self.directory)
        self.paramiko = import_paramiko()
        self._ssh_client_mock = patch("%s.SSHClient" % self.paramiko.__name__)
        self.ssh_client_mock = self._ssh_client_mock.start()
        self._ssh_config_mock = patch("%s.SSHConfig" % self.paramiko.__name__)
        self.ssh_config_mock = self._ssh_config_mock.start()
        self.ssh_config_mock().lookup.return_value = {}
        self._os_execvp_mock = patch("os.execvp")
        self.os_execvp_mock = self._os_execvp_mock.start()

    def tearDown(self):
        self.os_execvp_mock = self._os_execvp_mock.stop()
        del self.os_execvp_mock
        self.ssh_config_mock = self._ssh_config_mock.stop()
        del self.ssh_config_mock
        self.ssh_client_mock = self._ssh_client_mock.stop()
        del self.ssh_client_mock
        shutil.rmtree(self.directory)
        del self.directory

    def _write_config(self, content):
        with open(os.path.join(self.directory, 'aws.conf'), 'w') as f:
            f.write(content)

    def testInstanceHasNoStatus(self):
        self._write_config('\n'.join([
            '[plain-instance:foo]']))
        with patch('sys.stderr') as StdErrMock:
            with pytest.raises(SystemExit):
                self.aws(['./bin/aws', 'status', 'foo'])
        output = "".join(x[0][0] for x in StdErrMock.write.call_args_list)
        self.assertIn("invalid choice: 'foo'", output)

    def testInstanceCantBeStarted(self):
        self._write_config('\n'.join([
            '[plain-instance:foo]']))
        with patch('sys.stderr') as StdErrMock:
            with pytest.raises(SystemExit):
                self.aws(['./bin/aws', 'start', 'foo'])
        output = "".join(x[0][0] for x in StdErrMock.write.call_args_list)
        self.assertIn("invalid choice: 'foo'", output)

    def testInstanceCantBeStopped(self):
        self._write_config('\n'.join([
            '[plain-instance:foo]']))
        with patch('sys.stderr') as StdErrMock:
            with pytest.raises(SystemExit):
                self.aws(['./bin/aws', 'stop', 'foo'])
        output = "".join(x[0][0] for x in StdErrMock.write.call_args_list)
        self.assertIn("invalid choice: 'foo'", output)

    def testInstanceCantBeTerminated(self):
        self._write_config('\n'.join([
            '[plain-instance:foo]']))
        with patch('sys.stderr') as StdErrMock:
            with pytest.raises(SystemExit):
                self.aws(['./bin/aws', 'stop', 'foo'])
        output = "".join(x[0][0] for x in StdErrMock.write.call_args_list)
        self.assertIn("invalid choice: 'foo'", output)

    def testSSHWithNoHost(self):
        self._write_config('\n'.join([
            '[plain-instance:foo]']))
        with patch('mr.awsome.log') as LogMock:
            with pytest.raises(SystemExit):
                self.aws(['./bin/aws', 'ssh', 'foo'])
        self.assertEquals(
            LogMock.error.call_args_list, [
                (("Couldn't validate fingerprint for ssh connection.",), {}),
                (("No host or ip set in config.",), {}),
                (('Is the server finished starting up?',), {})])

    def testSSHWithFingerprintMismatch(self):
        self._write_config('\n'.join([
            '[plain-instance:foo]',
            'host = localhost',
            'fingerprint = foo']))
        self.ssh_client_mock().connect.side_effect = self.paramiko.SSHException(
            "Fingerprint doesn't match for localhost (got bar, expected foo)")
        with patch('mr.awsome.log') as LogMock:
            with pytest.raises(SystemExit):
                self.aws(['./bin/aws', 'ssh', 'foo'])
        self.assertEquals(
            LogMock.error.call_args_list, [
                (("Couldn't validate fingerprint for ssh connection.",), {}),
                (("Fingerprint doesn't match for localhost (got bar, expected foo)",), {}),
                (('Is the server finished starting up?',), {})])

    def testSSH(self):
        self._write_config('\n'.join([
            '[plain-instance:foo]',
            'host = localhost',
            'fingerprint = foo']))
        try:
            self.aws(['./bin/aws', 'ssh', 'foo'])
        except SystemExit:  # pragma: no cover - only if something is wrong
            self.fail("SystemExit raised")
        known_hosts = os.path.join(self.directory, 'known_hosts')
        self.os_execvp_mock.assert_called_with(
            'ssh',
            ['ssh', '-o', 'UserKnownHostsFile=%s' % known_hosts, '-l', 'root', '-p', '22', 'localhost'])


@pytest.yield_fixture
def tempdir():
    directory = tempfile.mkdtemp()
    yield directory
    shutil.rmtree(directory)


@pytest.fixture
def paramiko():
    from mr.awsome.common import import_paramiko
    return import_paramiko()


@pytest.yield_fixture
def sshconfig(paramiko):
    with patch("%s.SSHConfig" % paramiko.__name__) as ssh_config_mock:
        ssh_config_mock().lookup.return_value = {}
        yield ssh_config_mock


@pytest.yield_fixture
def sshclient(paramiko):
    with patch("%s.SSHClient" % paramiko.__name__) as ssh_client_mock:
        yield ssh_client_mock


@pytest.fixture
def instance(tempdir, sshconfig):
    configfile = os.path.join(tempdir, 'aws.conf')
    with open(configfile, 'w') as f:
        f.write('\n'.join([
            '[plain-instance:foo]',
            '[plain-instance:master]',
            'host=example.com',
            'fingerprint=master']))
    aws = AWS(tempdir)
    aws.configfile = os.path.join(tempdir, 'aws.conf')
    return aws.instances['foo']


def test_conn_no_host(instance):
    with patch('mr.awsome.common.log') as LogMock:
        with pytest.raises(SystemExit):
            instance.conn
    assert LogMock.error.call_args_list == [
        (("Couldn't connect to plain-instance:foo.",), {}),
        (("No host or ip set in config.",), {})]


def test_conn_no_fingerprint(instance):
    instance.config['host'] = 'localhost'
    with patch('mr.awsome.common.log') as LogMock:
        with pytest.raises(SystemExit):
            instance.conn
    assert LogMock.error.call_args_list == [
        (("Couldn't connect to plain-instance:foo.",), {}),
        (("No fingerprint set in config.",), {})]


def test_conn_fingerprint_mismatch(instance, paramiko, sshclient):
    instance.config['host'] = 'localhost'
    instance.config['fingerprint'] = 'foo'
    sshclient().connect.side_effect = paramiko.SSHException(
        "Fingerprint doesn't match for localhost (got bar, expected foo)")
    with patch('mr.awsome.common.log') as CommonLogMock:
        with patch('mr.awsome.plain.log') as PlainLogMock:
            with pytest.raises(SystemExit):
                instance.conn
    assert CommonLogMock.error.call_args_list == [
        (("Couldn't connect to plain-instance:foo.",), {}),
        (("Fingerprint doesn't match for localhost (got bar, expected foo)",), {})]
    assert PlainLogMock.error.call_args_list == [
        (("Failed to connect to foo (localhost)",), {}),
        (("username: 'root'",), {}),
        (("port: 22",), {})]


def test_conn(instance, sshclient):
    instance.config['host'] = 'localhost'
    instance.config['fingerprint'] = 'foo'
    conn = instance.conn
    assert len(conn.method_calls) == 3
    assert conn.method_calls[0][0] == 'set_missing_host_key_policy'
    assert conn.method_calls[1] == call.connect('localhost', username='root', key_filename=None, password=None, sock=None, port=22)
    assert conn.method_calls[2] == call.save_host_keys(instance.master.known_hosts)


def test_conn_cached(instance, sshclient):
    instance.config['host'] = 'localhost'
    instance.config['fingerprint'] = 'foo'
    first_client = MagicMock()
    second_client = MagicMock()
    sshclient.side_effect = [first_client, second_client]
    conn = instance.conn
    assert len(first_client.method_calls) == 3
    assert [x[0] for x in first_client.method_calls] == [
        'set_missing_host_key_policy',
        'connect',
        'save_host_keys']
    conn1 = instance.conn
    assert conn1 is conn
    assert conn1 is first_client
    assert conn1 is not second_client
    assert len(first_client.method_calls) == 4
    assert [x[0] for x in first_client.method_calls] == [
        'set_missing_host_key_policy',
        'connect',
        'save_host_keys',
        'get_transport']


def test_conn_cached_closed(instance, sshclient):
    instance.config['host'] = 'localhost'
    instance.config['fingerprint'] = 'foo'
    first_client = MagicMock()
    first_client.get_transport.return_value = None
    second_client = MagicMock()
    sshclient.side_effect = [first_client, second_client]
    conn = instance.conn
    assert len(first_client.method_calls) == 3
    assert [x[0] for x in first_client.method_calls] == [
        'set_missing_host_key_policy',
        'connect',
        'save_host_keys']
    conn1 = instance.conn
    assert conn1 is not conn
    assert conn1 is not first_client
    assert conn1 is second_client
    assert len(first_client.method_calls) == 4
    assert [x[0] for x in first_client.method_calls] == [
        'set_missing_host_key_policy',
        'connect',
        'save_host_keys',
        'get_transport']
    assert len(second_client.method_calls) == 3
    assert second_client.method_calls[0][0] == 'set_missing_host_key_policy'
    assert second_client.method_calls[1] == call.connect('localhost', username='root', key_filename=None, password=None, sock=None, port=22)
    assert second_client.method_calls[2] == call.save_host_keys(instance.master.known_hosts)


def test_bad_hostkey(instance, paramiko):
    with open(instance.master.known_hosts, 'w') as f:
        f.write('foo')
    instance.config['host'] = 'localhost'
    instance.config['fingerprint'] = 'foo'
    with patch("%s.SSHClient.connect" % paramiko.__name__) as connect_mock:
        connect_mock.side_effect = [
            paramiko.BadHostKeyException('localhost', 'bar', 'foo'),
            None]
        instance.init_ssh_key()
    assert os.path.exists(instance.master.known_hosts)
    with open(instance.master.known_hosts) as f:
        assert f.read() == ''


def test_proxycommand(instance, paramiko, sshclient, tempdir):
    with open(instance.master.known_hosts, 'w') as f:
        f.write('foo')
    instance.config['host'] = 'localhost'
    instance.config['fingerprint'] = 'foo'
    instance.config['proxycommand'] = 'nohup {path}/../bin/assh {instances[foo].host} -o UserKnownHostsFile={known_hosts}'
    with patch("%s.ProxyCommand" % paramiko.__name__) as ProxyCommandMock:
        info = instance.init_ssh_key()
    proxycommand = 'nohup %s/../bin/assh localhost -o UserKnownHostsFile=%s' % (tempdir, instance.master.known_hosts)
    assert info['ProxyCommand'] == proxycommand
    assert ProxyCommandMock.call_args_list == [call(proxycommand)]


def test_proxyhost(instance, paramiko, sshclient, tempdir):
    with open(instance.master.known_hosts, 'w') as f:
        f.write('foo')
    instance.config['host'] = 'localhost'
    instance.config['fingerprint'] = 'foo'
    instance.config['proxyhost'] = 'master'
    client = MagicMock()
    master = MagicMock()
    sshclient.side_effect = [client, master]
    with patch("%s.ProxyCommand" % paramiko.__name__) as ProxyCommandMock:
        info = instance.init_ssh_key()
    assert 'ProxyCommand' not in info
    assert not ProxyCommandMock.called
    assert len(client.method_calls) == 4
    assert client.method_calls[0][0] == 'set_missing_host_key_policy'
    assert client.method_calls[1] == call.load_host_keys(instance.master.known_hosts)
    assert client.method_calls[2][0] == 'connect'
    assert client.method_calls[2][1] == ('localhost',)
    assert client.method_calls[2][2].get('sock') is not None
    kwargs_without_sock = dict((k, v) for k, v in client.method_calls[2][2].items() if k != 'sock')
    assert kwargs_without_sock == dict(username='root', key_filename=None, password=None, port=22)
    assert client.method_calls[3] == call.save_host_keys(instance.master.known_hosts)
    assert len(master.method_calls) == 5
    assert master.method_calls[0][0] == 'set_missing_host_key_policy'
    assert master.method_calls[1] == call.load_host_keys(instance.master.known_hosts)
    assert master.method_calls[2] == call.connect('example.com', username='root', key_filename=None, password=None, sock=None, port=22)
    assert master.method_calls[3] == call.save_host_keys(instance.master.known_hosts)
    assert master.method_calls[4] == call.get_transport()


def test_missing_host_key_mismatch(paramiko, sshclient):
    from mr.awsome.plain import ServerHostKeyPolicy
    shkp = ServerHostKeyPolicy(lambda: '66:6f:6f')  # that's 'foo' as hex
    key = MagicMock()
    key.get_fingerprint.return_value = 'bar'
    with pytest.raises(paramiko.SSHException) as e:
        shkp.missing_host_key(sshclient, 'localhost', key)
    assert e.value.message == "Fingerprint doesn't match for localhost (got 62:61:72, expected 66:6f:6f)"


def test_missing_host_key(tempdir, sshclient):
    from mr.awsome.plain import ServerHostKeyPolicy
    known_hosts = os.path.join(tempdir, 'known_hosts')
    sshclient._host_keys_filename = known_hosts
    shkp = ServerHostKeyPolicy(lambda: '66:6f:6f')  # that's 'foo' as hex
    key = MagicMock()
    key.get_fingerprint.return_value = 'foo'
    key.get_name.return_value = 'ssh-rsa'
    shkp.missing_host_key(sshclient, 'localhost', key)
    assert sshclient.method_calls == [
        call._host_keys.add('localhost', 'ssh-rsa', key),
        call.save_host_keys(known_hosts)]


def test_missing_host_key_ignore(tempdir, sshclient):
    from mr.awsome.plain import ServerHostKeyPolicy
    known_hosts = os.path.join(tempdir, 'known_hosts')
    sshclient._host_keys_filename = known_hosts
    shkp = ServerHostKeyPolicy(lambda: 'ignore')
    key = MagicMock()
    key.get_fingerprint.return_value = 'foo'
    key.get_name.return_value = 'ssh-rsa'
    with patch('mr.awsome.plain.log') as LogMock:
        shkp.missing_host_key(sshclient, 'localhost', key)
    assert sshclient.method_calls == [
        call._host_keys.add('localhost', 'ssh-rsa', key),
        call.save_host_keys(known_hosts)]
    assert LogMock.method_calls == [
        call.warn('Fingerprint verification disabled!')]


def test_missing_host_key_ask_answer_no(tempdir, sshclient):
    from mr.awsome.plain import ServerHostKeyPolicy
    known_hosts = os.path.join(tempdir, 'known_hosts')
    sshclient._host_keys_filename = known_hosts
    shkp = ServerHostKeyPolicy(lambda: 'ask')
    key = MagicMock()
    key.get_fingerprint.return_value = 'foo'
    key.get_name.return_value = 'ssh-rsa'
    with patch("mr.awsome.plain.yesno") as yesno_mock:
        yesno_mock.return_value = False
        with pytest.raises(SystemExit):
            shkp.missing_host_key(sshclient, 'localhost', key)


def test_missing_host_key_ask_answer_yes(tempdir, sshclient):
    from mr.awsome.plain import ServerHostKeyPolicy
    known_hosts = os.path.join(tempdir, 'known_hosts')
    sshclient._host_keys_filename = known_hosts
    shkp = ServerHostKeyPolicy(lambda: 'ask')
    key = MagicMock()
    key.get_fingerprint.return_value = 'foo'
    key.get_name.return_value = 'ssh-rsa'
    with patch("mr.awsome.plain.yesno") as yesno_mock:
        yesno_mock.return_value = True
        shkp.missing_host_key(sshclient, 'localhost', key)
    assert sshclient.method_calls == []


def test_missing_host_key_ask_answer_yes_and_try_again(tempdir, sshclient):
    from mr.awsome.plain import ServerHostKeyPolicy
    known_hosts = os.path.join(tempdir, 'known_hosts')
    sshclient._host_keys_filename = known_hosts
    shkp = ServerHostKeyPolicy(lambda: 'ask')
    key = MagicMock()
    key.get_fingerprint.return_value = 'foo'
    key.get_name.return_value = 'ssh-rsa'
    with patch("mr.awsome.plain.yesno") as yesno_mock:
        # if yesno is called twice, it throws an error
        yesno_mock.side_effect = [True, RuntimeError]
        shkp.missing_host_key(sshclient, 'localhost', key)
        shkp.missing_host_key(sshclient, 'localhost', key)
    assert sshclient.method_calls == []
