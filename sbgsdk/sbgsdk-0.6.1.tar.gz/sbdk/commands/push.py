import json
import os.path
import requests
import logging
from sys import exit

from sbdk.auth import push_url, push_json
from sbdk.commands import check_project_dir, check_image, check_project_data
from sbdk.docker import make_runner
from sbdk.error import SbdkError
from sbdk.docker.container import dockerize


def argument_parser(subparsers):
    parser = subparsers.add_parser("push", help="Create new image and upload it")
    parser.set_defaults(func=push)
    parser.add_argument('message', help='Short description of your changes')


def push(project, message, retries=2, container=None):
    if retries < 0:
        container.remove()
        raise SbdkError('Push command failed')
    check_project_dir(project)
    check_project_data(project)
    check_image(project)

    if not container:
        docker = make_runner(project)
        container = docker.run_install()
        if not container.is_success():
            print("Error while preparing image:")
            container.print_log()
            exit("Push command failed")
    config = {'Cmd': project.sdk_runner_command, 'Entrypoint': project.docker_entrypoint}
    container.load_credentials(renew=False)
    if not container.check_privilege():
        print('You do not have permissions to push into repository. Try again:')
        container.load_credentials(renew=True)
        if not container.check_privilege():
            container.remove()
            raise SbdkError('You do not have permissions to push into repository')
    container.commit(message, config).push()
    if not check_container_push(container):
        retry = raw_input('Push failed, image not found in registry. Try again? [Y/n]: ').lower().strip()
        if retry == '' or retry == 'y':
            push(project, message, retries-1, container)
        elif retry == 'n':
            container.remove()
            exit("Push command failed")
    push_schema(project, container)
    container.remove()


def push_schema(project, container):
    data_dir = project.project_data
    # nulling project_data to force image runner
    project.project_data = None
    project.image_id = container.image['Id']
    runner = make_runner(project)
    runner.schema('.sbdk/schema.json', remove=True)

    with open(os.path.join(data_dir, 'schema.json')) as fp:
        wrapper_data = json.load(fp)  # json.loads(self.docker.logs(c))

    if not wrapper_data:
        print('No wrappers registered (empty __init__.py?). Exiting.')
        exit(1)

    push_data = {'message': container.message or 'NO COMMIT MESSAGE',
                 'image_data': {'id': container.repository,
                                'tag': container.tag},
                 'wrappers': wrapper_data}

    if project.schema_server_url:
        url = push_url(project, dockerize(project.state['username']))
        try:
            push_json(url, push_data, container.token)
        except requests.HTTPError as e:
            if e.response.status_code in (401, 402):
                container.load_credentials()
                push_json(url, push_data, container.token)
            else:
                raise e


def check_container_push(container, retries=2):
    if retries < 0:
        return False
    docker_repo, image_id = container.repository, container.tag

    check_image = requests.get('%s://%s/v1/repositories/%s/%s/images'
                               % tuple([container.project.docker_registry_schema] + docker_repo.split('/')))
    check_tag = requests.get('%s://%s/v1/repositories/%s/%s/tags'
                             % tuple([container.project.docker_registry_schema] + docker_repo.split('/')))
    if check_image.status_code != 200:
        raise Exception('Bad response (%s) : %s' % (check_image.status_code, check_image.content))
    if check_tag.status_code != 200:
        raise Exception('Bad response (%s) : %s' % (check_tag.status_code, check_tag.content))
    if any(image_id in tag for tag in [i['id'] for i in check_image.json()]):
        if image_id in check_tag.json().keys():
            logging.debug('Image pushed successfuly')
            return True
        else:
            logging.debug('Image pushed but not taged. Trying again: Retry left: %s' % str(retries))
            container.push()
            return check_container_push(container, retries-1)

