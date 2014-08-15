import os
import yaml
import json
import shutil
import re
import click
import requests
import hexlet
import subprocess
from hexlet import commands, routes, utils
from hexlet.commands import shared
from pprintpp import pformat
import dist

@click.command(help="init lesson directory")
@click.argument('lesson_name')
@click.argument('language')
@commands.shared_handling
def init(ctx, logger, t, lesson_name, language):
    cwd = os.getcwd()
    lesson_folder = "{lesson_name}_{language}_lesson".format(lesson_name=lesson_name, language=language)
    if os.path.isdir(lesson_folder):
        ctx.fail(t(".folder_already_exists", folder=lesson_folder))
    else:
        shutil.copytree(hexlet.lesson_skeleton_path, lesson_folder)
        logger.info(t(".lesson_created", folder=lesson_folder))


@click.command(help="See hexlet_api_key in your site profile")
@click.argument('hexlet_api_key')
@commands.shared_handling
def login(ctx, logger, t, hexlet_api_key):
    url = routes.api_teacher_check_auth_url(host=ctx.obj["host"])
    logger.debug(url)
    shared.login(ctx, logger, t, url, hexlet_api_key)


@click.command(help="submit lesson to server")
@click.argument("path", type=click.Path(exists=True, resolve_path=True))
@commands.check_logged_in
@commands.shared_handling
def submit(ctx, logger, t, path):
    lesson_folder = os.path.split(path)[-1]

    try:
        (slug, locale, kind) = lesson_folder.rsplit("_", 2)
    except:
        ctx.fail(t(".wrong_folder_name", folder=lesson_folder))

    if kind == "lesson":
        submit_lesson(ctx, logger, t, path, slug, locale)
    else:
        ctx.fail(t(".wrong_folder_name", folder=lesson_folder))


def submit_lesson(ctx, logger, t, path, slug, locale):
    host = ctx.obj["host"]
    tarball_path = dist.generate_lesson_tarball(path)

    payload = {
            "lesson": {
                "slug": slug,
                "locale": locale
                }
            }

    files = {"lesson[packs_attributes][0][tarball]": open(tarball_path, "rb")}

    url = routes.api_teacher_lessons_url(host=host)
    logger.debug(url)
    # headers = {'Content-Type': 'application/json'}
    headers = {}
    headers.update(utils.get_api_key_header())

    res = requests.post(
            url,
            data=utils.build_key_value(payload),
            headers=headers,
            files=files,
            timeout=5)
    if res.status_code == 201:
        logger.info(t(".lesson_uploaded", lesson=slug))
    else:
        logger.debug(pformat(res))
        logger.debug(pformat(res.text))
        ctx.fail(t(".lesson_upload_failure"))

#     def generate_terminals():
#         terminal_path = os.path.join(path, "terminal")
#         try:
#             cmd = ["make", "generate", "-C", terminal_path]
#             p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#             out, err = p.communicate()
#         except OSError:
#             ctx.fail(t(".could_not_generate_terminals"))

#         if p.returncode:
#             logger.debug(pformat(cmd))
#             logger.debug(pformat(out))
#             logger.debug(pformat(err))
#             ctx.fail(t(".terminal_generation_failed"))

#     def run_tests(test_path):
#         try:
#             unit = test_path.split(os.sep)[-1]
#             cmd = ["make", "test", "-C", test_path]
#             p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#             out, err = p.communicate()
#         except OSError:
#             ctx.fail(t(".could_not_run_tests", unit=unit))

#         if p.returncode:
#             logger.debug(pformat(cmd))
#             logger.debug(pformat(out))
#             logger.debug(pformat(err))
#             ctx.fail(t(".tests_failed", unit=unit))

#     def run_code_tests():
#         code_path = os.path.join(path, "code")
#         code_dist_path = os.path.join(code_path, "dist")
#         if os.path.isdir(code_dist_path):
#             shutil.rmtree(code_dist_path)

#         run_tests(code_path)

#     def run_codex_tests():
#         codex_path = os.path.join(path, "codex")
#         run_tests(codex_path)

@click.group()
@click.option('--host', type=click.STRING, default=hexlet.host, help="another-host.io")
@click.option('-v', '--verbose', count=True)
@click.pass_context
def cli(ctx, host, verbose):
    ctx.obj = {
        "host": host,
        "verbose": verbose,
    }

cli.add_command(login)
cli.add_command(submit)
cli.add_command(init)
