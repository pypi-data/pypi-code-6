# coding:utf-8
from flask import Flask

from casslr.lib.szradm import FarmRoleEngine

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8020

app = Flask(__name__)
app.config.update({
    "ENGINE": FarmRoleEngine,
})


@app.route('/seeds')
def hello_world():
    engine = app.config["ENGINE"]
    farm_role_id = engine.current_farm_role_id()
    farm_role = engine.farm_role_by_id(farm_role_id)

    seeds_by_location = {}
    for server in farm_role.running_servers:
        if server.location not in seeds_by_location:
            seeds_by_location[server.location] = server.internal_ip
    return ",".join(seeds_by_location.values())


if __name__ == '__main__':
    app.run(host=DEFAULT_HOST, port=DEFAULT_PORT)

