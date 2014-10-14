from .liveserver import LiveServer
from .main import app, Message


def before_all(context):
    context.live_server = LiveServer(app)
    context.live_server.start()

    context.url = context.live_server.url


def after_all(context):
    context.live_server.stop()


def before_scenario(context, scenario):
    context.headers = {}


def after_scenario(context, scenario):
    with app.app_context():
        Message.objects.collection.remove()
