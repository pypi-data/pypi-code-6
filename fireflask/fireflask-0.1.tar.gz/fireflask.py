
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
from firepython.middleware import FirePythonWSGI, logging

def FireFlask(app):
    """
    Configure logging to go through FirePython, and to include
    all levels messages of level DEBUG or higher (generally, 
    everything, since DEBUG < INFO < WARNING < ERROR < CRITICAL)
    """

    app.wsgi_app = FirePythonWSGI(app.wsgi_app)
    logging.getLogger().setLevel(DEBUG)
    return app
