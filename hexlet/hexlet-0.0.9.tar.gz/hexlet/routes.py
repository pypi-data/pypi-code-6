from purl import URL
import hexlet

def generate_url(func):
    def inner(*args, **kwargs):
        uri = func(*args)
        api_type = func.__name__.split("_")

        host = hexlet.host
        if "host" in kwargs:
            host = kwargs["host"]

        u = URL(scheme='http', host=host) \
                .path('api_%s/%s' % (api_type[1], uri)) \

        if "hexlet_api_key" in kwargs:
            u = u.query_param('hexlet_api_key', kwargs["hexlet_api_key"])

        return u.as_string()
    return inner


@generate_url
def api_teacher_check_auth_url():
    return "user/check_auth.json"


@generate_url
def api_member_check_auth_url():
    return "user/check_auth.json"


@generate_url
def api_teacher_lesson_versions_url(lesson_id):
    return "lessons/%s/versions" % lesson_id


@generate_url
def api_teacher_lessons_url():
    return "lessons"


@generate_url
def api_teacher_courses_url():
    return "courses"
