# -*- coding: utf-8 -*-
"""
    tlutil.factory
"""


import pkgutil
import importlib

from flask import Flask, Blueprint


__all__ = [
    "register_blueprints", "create_app"
]


def register_blueprints(app, package_name, package_path):
    """自动寻找Blueprint
    :param app: Flask应用
    :param package_name: 子应用包名
    :param package_path: 子应用包路径
    """
    rv = []
    for _, name, _ in pkgutil.iter_modules(package_path):
        m = importlib.import_module("%s.%s" % (package_name, name))
        for item in dir(m):
            item = getattr(m, item)
            if isinstance(item, Blueprint):
                app.register_blueprint(item)
            rv.append(item)
    return rv


def create_app(app_name, package_name, package_path, settings_override=None):
    """创建项目
    :param app_name: 项目包名
    :param package_name: 子应用包名
    :param package_path: 子应用包路径
    :param settings_override: 重载配置
    """
    app = Flask(package_name)

    app.config.from_object("%s.configs" % (app_name))
    app.config.from_pyfile("configs.py", silent=True)
    app.config.from_object(settings_override)

    register_blueprints(app, package_name, package_path)
    return app
