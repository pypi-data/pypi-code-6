from sbdk.commands import check_image, check_project_dir
from sbdk.docker import make_runner


def argument_parser(subparsers):
    parser = subparsers.add_parser("test", help="Test wrapper")
    parser.set_defaults(func=test)
    parser.add_argument("module", help="Python module with tests. E.g. 'sbg_wrappers.my_wrapper'. "
                                       "Same as nosetests '--where'", type=str, default='.')
    parser.add_argument("--keep-container", "-k", help="Don't remove container when run finishes", type=bool)


def test(project, module, keep_container=False):
    check_project_dir(project)
    check_image(project)
    r = make_runner(project)
    try:
        r.run_tests(module, remove=not keep_container)
    finally:
        c = r.chown()
        c.remove()


__test__ = False

