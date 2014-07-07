import click
import requests
from hexlet import commands, routes, utils

def login(ctx, logger, t, url, hexlet_api_key):
    res = requests.get(url)
    logger.debug(res)

    if res.status_code == 200:
        data = {
            "hexlet_api_key": hexlet_api_key
        }

        utils.write_config(data)

        logger.info(t(".login_successful"))
        logger.info(t(".file_written", file_name=utils.config_path))

    elif res.status_code == 403:
        ctx.fail(t(".invalid_credentials"))
    else:
        ctx.fail(t(".smth_wrong"))
