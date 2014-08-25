from sbdk.commands import check_project_dir, check_project_data, check_project_state
from sbdk.auth import update_docker_cfg
from docker.auth.auth import load_config

def argument_parser(subparsers):
    parser = subparsers.add_parser("logout", help="Login to docker registry")
    parser.set_defaults(func=registry_logout)

def registry_logout(project):
    check_project_dir(project)
    check_project_data(project)
    check_project_state(project)

    cfg = load_config()
    if project.docker_registry_url in cfg:
        del cfg[project.docker_registry_url]

    update_docker_cfg(cfg)

