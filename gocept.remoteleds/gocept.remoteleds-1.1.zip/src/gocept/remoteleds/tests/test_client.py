import gocept.remoteleds.client
import gocept.remoteleds.jenkins
import mock


def test_client_update_calls_sendstate():
    project = gocept.remoteleds.client.Project('backy', 0)
    client = gocept.remoteleds.jenkins.JenkinsClient(
        None, {'baseurl': 'https://builds.gocept.com',
               'user': None, 'password': None, 'projects': [project]})
    with mock.patch('gocept.remoteleds.client.Client.send_state') as method:
        client.update(100)
        method.assert_called_once_with(None, project)
