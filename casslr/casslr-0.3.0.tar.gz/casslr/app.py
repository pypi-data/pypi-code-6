# coding:utf-8
from flask import Flask

from casslr.szradm import FarmRoleEngine

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8020

# 0-indexed server IDs that are modulo this number are used as seeds.
# Server #1 is guaranteed to be among seed nodes.
# This should be a stricly positive integer
DEFAULT_SEED_MODULO = 3

app = Flask(__name__)
app.config.update({
    "ENGINE": FarmRoleEngine(),
    "SEED_MODULO": DEFAULT_SEED_MODULO,
})


@app.route('/seeds')
def seeds():
    engine = app.config["ENGINE"]
    farm_role_id = engine.current_farm_role_id()
    farm_role = engine.farm_role_by_id(farm_role_id)

    seeds = []

    for server in farm_role.running_servers:
        if (server.index - 1) % app.config["SEED_MODULO"] == 0:  # 1-indexed to 0-indexed
            seeds.append(server.internal_ip)

    return ",".join(seeds)

@app.route('/status')
def status():
    return "OK"


if __name__ == '__main__':
    app.run(host=DEFAULT_HOST, port=DEFAULT_PORT)

