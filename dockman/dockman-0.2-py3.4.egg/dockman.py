import json

import docker
from flask import Flask, request, abort


app = Flask(__name__)


def load_repos():
    with open(app.config['DOCKER_REPOS']) as fp:
        return json.load(fp)

app.config.from_envvar('DOCKMAN_CONFIG')
app.config['DOCKER_REPOS'] = load_repos()

client = docker.Client(base_url='unix://var/run/docker.sock',
                       version='1.12',
                       timeout=60)


def safe_remove_container(container_name):
    client.stop(container_name)
    client.remove_container(container_name)


def container_exists(container_name, containers):
    # for some reason the container list prepends /
    listed_name = '/' + container_name
    return any([listed_name in c['Names'] for c in containers])


@app.route('/', methods=['POST'])
def docker_hook():
    d = None
    try:
        d = request.get_json(force=True)
    except Exception as e:
        app.logger.error('Error loading json', e)
        abort(400)
    if d:
        repo_name = d['repository']['repo_name']
        container = app.config.get('DOCKER_REPOS', {}).get(repo_name)
        if docker:
            resp_stream = client.build(path=container['dockerfile_path'],
                                       tag=container['tag'])
            [resp_stream]  # block on stream
            containers = client.containers(all=True)
            if container_exists(container['name'], containers):
                safe_remove_container(container['name'])
            client.create_container(container['tag'], name=container['name'])
            client.start(container['name'])
            return '', 200
        else:
            abort(403)
