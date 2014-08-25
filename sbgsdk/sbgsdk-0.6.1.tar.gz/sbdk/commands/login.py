from sbdk.commands import check_project_dir, check_project_data, check_project_state
from sbdk.auth import login, store_credentials
from docker.auth.auth import load_config

def argument_parser(subparsers):
    parser = subparsers.add_parser("login", help="Login to docker registry")
    parser.set_defaults(func=registry_login)


def registry_login(project):
    check_project_dir(project)
    check_project_data(project)
    check_project_state(project)

    print project.schema_server_url
    cfg = load_config()
    user, token = login(project)

    store_credentials(project.docker_registry_url, user, token, cfg)


