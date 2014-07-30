# coding:utf-8
import os
import logging

from flask import Flask, request

from casslr.szradm import FarmRoleEngine

logger = logging.getLogger(__name__)


CONFIG_PATH = os.environ.get('CASSLR_CONFIG_FILE', '/etc/casslr.cfg')

# 0-indexed server IDs that are modulo this number are used as seeds.
# Server #1 is guaranteed to be among seed nodes.
# This should be a stricly positive integer
DEFAULT_SEED_MODULO = 3

app = Flask(__name__)
app.config.update({
    "ENGINE": FarmRoleEngine(),
    "SEED_MODULO": DEFAULT_SEED_MODULO,
    "LOG_FILE": None,
    "LOG_LEVEL": logging.INFO
})

# Try to load the config, fail silently if it's not there
app.config.from_pyfile(CONFIG_PATH, True)

if app.config["LOG_FILE"]:
    log_level = app.config["LOG_LEVEL"]

    if log_level <= logging.DEBUG:
        log_format = "[%(pathname)s] %(asctime)s %(levelname)s in [%(name)s]: %(message)s"
    else:
        log_format = "%(asctime)s %(levelname)s in [%(name)s]: %(message)s"

    file_handler = logging.FileHandler(app.config['LOG_FILE'])
    file_handler.setFormatter(logging.Formatter(log_format))

    for l in (app.logger, logging.getLogger('casslr')):
        l.setLevel(log_level)
        l.addHandler(file_handler)


@app.route('/seeds')
def seeds():
    logger.debug("Received seed request: %s", request)

    engine = app.config["ENGINE"]
    farm_role_id = engine.current_farm_role_id()
    farm_role = engine.farm_role_by_id(farm_role_id)

    seeds = []

    for server in farm_role.running_servers:
        if (server.index - 1) % app.config["SEED_MODULO"] == 0:  # 1-indexed to 0-indexed
            seeds.append(server.internal_ip)

    app.logger.info("Seeds: `%s`", seeds)

    return ",".join(seeds)

@app.route('/status')
def status():
    return "OK"


if __name__ == '__main__':
    DEFAULT_HOST = "127.0.0.1"
    DEFAULT_PORT = 8020
    app.run(host=DEFAULT_HOST, port=DEFAULT_PORT)

