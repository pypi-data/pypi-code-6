from purl import URL
import hexlet
import utils

def generate_url(func):
    def inner(*args, **kwargs):
        uri = func(*args)
        api_type = func.__name__.split("_")

        host = hexlet.host
        if "host" in kwargs:
            host = kwargs["host"]

        u = URL(scheme='http', host=host) \
                .path('api_%s/%s' % (api_type[1], uri)) \

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
    return "lessons/%s/versions.json" % lesson_id


@generate_url
def api_teacher_lessons_url():
    return "lessons.json"


@generate_url
def api_member_exercise_url(lesson_id):
    return "lessons/%s/exercise" % lesson_id
