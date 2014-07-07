import requests, os, json, pytest, i18n, pkg_resources

@pytest.fixture(scope="module")
def t():
    def func(message, **kwargs):
        return i18n.t(message, **kwargs)
    return func

#
# Helpers for commands
#
def generate_fixture_path(part):
    return os.path.join(os.path.dirname(__file__), "fixtures", part)

def prepare_request_mock(status_code):
    def func(*args, **kwargs):
        r = requests.Response()
        r.status_code = status_code
        return r
    return func

def prepare_lesson_submit_mock(step):
    def func(*args, **kwargs):
        r = requests.Response()
        if "data" in kwargs.keys():
            data = kwargs["data"]
            if step == "upload_course" and "course[slug]" in data.keys() or \
               step == "upload_lesson" and "lesson" in json.loads(data).keys() or \
               step == "upload_lesson_version" and "lesson_version" in json.loads(data).keys():
                r.status_code = 500
            else:
                r.status_code = 201
        return r
    return func

#
# Helpers for test utils
#

def get_update_test_funcs(project_name, current_version, new_version, ret_empty_releases=False):
    def get_pipy_object(_url):
        class StubClass:
            def __init__(self):
                self.package_releases = lambda prj: [new_version] if not ret_empty_releases else None
        return StubClass()

    def get_installed_distributions():
        class StubClass:
            def __init__(self):
                self.project_name = project_name
                self.version = current_version
        return [StubClass()]
    return {"get_curr_ver_func": get_installed_distributions, "get_new_ver_func": get_pipy_object}
