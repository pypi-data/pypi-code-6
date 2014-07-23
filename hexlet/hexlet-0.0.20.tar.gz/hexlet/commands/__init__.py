import os
import zipfile
import subprocess
import yaml
import tarfile
import shutil
import re
import json
from functools import update_wrapper
import requests
import click
import inspect
import i18n

import hexlet
from hexlet import utils, exceptions


def shared_handling(f):
    @click.pass_context
    def wrapper(ctx, *args, **kwargs):
        logger = hexlet.Logger(verbose=ctx.obj["verbose"])
        def t(message, **kwargs):
            frame_records = inspect.stack()[1]
            calling_module = inspect.getmodulename(frame_records[1])

            #FIXME implement scopes in i18n
            key = "%s.%s.%s%s" % ("commands", calling_module, f.__name__, message)
            return i18n.t(key, **kwargs)
        try:
            return ctx.invoke(f, ctx, logger, t, *args, **kwargs)
        except exceptions.ManifestError:
            ctx.fail(i18n.t("main.wrong_manifest"))
        except requests.exceptions.ConnectionError:
            ctx.fail(i18n.t("main.connection_error"))

    return update_wrapper(wrapper, f)


def check_logged_in(f):
    @click.pass_context
    def wrapper(ctx, *args, **kwargs):
        if not os.path.isfile(utils.get_config_path()):
            ctx.fail(i18n.t("main.not_logged_in"))
        f(ctx, *args, **kwargs)
    return update_wrapper(wrapper, f)
