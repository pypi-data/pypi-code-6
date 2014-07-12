import click
import requests
import os
import tarfile
import io
import subprocess
import shutil
import re
import hexlet

from hexlet import commands, routes, utils
from hexlet.commands import shared
from contextlib import closing


@click.command()
@click.argument("hexlet_api_key")
@commands.shared_handling
def login(ctx, logger, t, hexlet_api_key):
    url = routes.api_member_check_auth_url(host=ctx.obj["host"],
                                           hexlet_api_key=hexlet_api_key)
    shared.login(ctx, logger, t, url, hexlet_api_key)


@click.command()
@click.argument("lesson_id")
@commands.shared_handling
def fetch(ctx, logger, t, lesson_id):
    url = routes.api_member_exercise_url(lesson_id,
                                         host=ctx.obj["host"],
                                         hexlet_api_key=utils.value_for("hexlet_api_key"))
    res = requests.get(url)
    if res.status_code == 200:
        lesson_dir_path = os.path.join(os.getcwd(), lesson_id)
        exercise_dir_path = os.path.join(lesson_dir_path, "code")

        if not os.path.isdir(lesson_dir_path):
            os.mkdir(lesson_dir_path)

        if not os.path.isdir(exercise_dir_path):
            os.mkdir(exercise_dir_path)

        with io.BytesIO(res.content) as bio:
            with closing(tarfile.open(fileobj=bio, mode="r:gz")) as tar:
                tar.extractall(exercise_dir_path)
        logger.info(t(".exercise_fetched", folder=lesson_id))
    else:
        ctx.fail(t(".exercise_fetch_failure"))


@click.command()
@click.argument("path", type=click.Path(exists=True, resolve_path=True))
@commands.shared_handling
def submit(ctx, logger, t, path):
    code_path = path
    lesson_id = code_path.split(os.sep)[-2]

    def run_tests():
        try:
            cmd = ["make", "test", "-C", code_path]
            p = subprocess.Popen(cmd, shell=False,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            out, err = p.communicate()
        except OSError:
            ctx.fail(t(".could_not_run_tests"))

        if p.returncode:
            ctx.fail(t(".tests_failed"))

    def create_tarball():
        tarball_path = os.path.join(code_path, "solution.tar.gz")
        if os.path.isfile(tarball_path):
            os.unlink(tarball_path)

        exclude_files = [".+\.pyc$"]
        exclude_dirs = [
            "node_modules",
            "bower_components",
            "coverage",
            ".tox"]
        with closing(tarfile.open(tarball_path, "w:gz")) as tar:
            for (dirpath, dirnames, filenames) in os.walk(code_path):
                dirnames[:] = [d for d in dirnames if d not in exclude_dirs]
                for filename in filenames:
                    if any(re.match(regexp, filename) for regexp in exclude_files):
                        continue
                    tar.add(os.path.join(dirpath, filename),
                            arcname=os.path.join(dirpath.replace(code_path, ""),
                                                 filename))
        return tarball_path

    def send_results(tarball_path):
        payload = {"exercise[passed]": 1}
        files = {"exercise[attach]": open(tarball_path, "rb")}
        url = routes.api_member_exercise_url(lesson_id,
                                             host=ctx.obj["host"],
                                             hexlet_api_key=utils.value_for("hexlet_api_key"))

        res = requests.post(
                        url,
                        data=payload,
                        files=files,
                        timeout=1)
        if res.status_code == 201:
            logger.info(t(".exercise_submitted"))
        else:
            ctx.fail(t(".exercise_submit_failure"))

    run_tests()
    tarball_path = create_tarball()
    send_results(tarball_path)


@click.group()
@click.option('--host', type=click.STRING, default=hexlet.host)
@click.option('-v', '--verbose', count=True)
@click.pass_context
def cli(ctx, host, verbose):
    ctx.obj = {
        "host": host,
        "verbose": verbose,
    }

cli.add_command(login)
cli.add_command(fetch)
cli.add_command(submit)
