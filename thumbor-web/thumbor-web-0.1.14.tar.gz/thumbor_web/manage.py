#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask.ext.script import Manager
from flask.ext.assets import ManageAssets

from thumbor_web.app import create_app
from thumbor_web.assets import assets_env


def main():
    app = create_app('./thumbor_web/config/local.conf')
    manager = Manager(app)
    manager.add_command("assets", ManageAssets(assets_env))
    manager.run()


if __name__ == "__main__":
    main()
