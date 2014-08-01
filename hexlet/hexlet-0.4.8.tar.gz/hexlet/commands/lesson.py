import os
import yaml
import json
import shutil
import tarfile
import re
import click
import requests
import hexlet
import subprocess
from hexlet import commands, routes, utils
from hexlet.commands import shared
from contextlib import closing
from pprintpp import pformat

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
        (name, locale, kind) = lesson_folder.rsplit("_", 2)
    except:
        ctx.fail(t(".wrong_folder_name", folder=lesson_folder))

    if kind == "lesson":
        submit_lesson(ctx, logger, t, path, name, locale)
    else:
        ctx.fail(t(".wrong_folder_name", folder=lesson_folder))


def submit_lesson(ctx, logger, t, path, name, locale):
    host = ctx.obj["host"]
    tarball_name = "lesson.tar.gz"
    dist_path = os.path.join(path, "dist")

    def upload_lesson():
        lesson_params = read_lesson_params()

        payload = {
            "lesson": lesson_params
        }
        payload["lesson"]["locale"] = locale

        url = routes.api_teacher_lessons_url(host=host)
        logger.debug(url)
        headers = {'Content-Type': 'application/json'}
        headers.update(utils.get_api_key_header())

        res = requests.post(
            url,
            data=json.dumps(payload),
            headers=headers,
            timeout=3)
        if res.status_code == 201:
            logger.info(t(".lesson_uploaded", lesson=name))
        else:
            logger.debug("response: code %d" % res.status_code)
            logger.debug("response: body %s" % res.text)
            ctx.fail(t(".lesson_upload_failure"))

    def upload_lesson_version():
        lesson_params = read_lesson_params()

        if "terminal" in lesson_params["units"]:
            generate_terminals()

        if "code" in lesson_params["units"]:
            generate_code_dist()

        if "codex" in lesson_params["units"]:
            run_codex_tests()

        tarball_path = create_tarball()
        files = {"lesson_version[tarball]": open(tarball_path, 'rb')}
        url = routes.api_teacher_lesson_versions_url(name, host=host)

        logger.debug(url)
        res = requests.post(
            url,
            headers=utils.get_api_key_header(),
            files=files,
            timeout=3)
        if res.status_code == 201:
            logger.info(t(".lesson_version_uploaded", version=name))
        else:
            ctx.fail(t(".lesson_version_upload_failure"))

    def read_lesson_params():
        lesson_manifest_path = os.path.join(path, "lesson.yml")
        return read_params(lesson_manifest_path)

    def read_code_params():
        code_manifest_path = os.path.join(path, "code", "main.yml")
        return read_params(code_manifest_path)

    def read_params(manifest_path):
        if not os.path.isfile(manifest_path):
            ctx.fail(t(
                ".file_not_exists",
                file=os.path.basename(manifest_path),
                path=os.path.dirname(manifest_path)))

        with open(manifest_path, "r") as stream:
            data = yaml.load(stream)
            data["slug"] = name

        return data

    def generate_terminals():
        terminal_path = os.path.join(path, "terminal")
        try:
            cmd = ["make", "generate", "-C", terminal_path]
            p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
        except OSError:
            ctx.fail(t(".could_not_generate_terminals"))

        if p.returncode:
            logger.debug(pformat(cmd))
            logger.debug(pformat(out))
            logger.debug(pformat(err))
            ctx.fail(t(".terminal_generation_failed"))

    def generate_code_dist():
        code_params = read_code_params()
        run_code_tests()
        create_code_tarball(code_params)

    def run_tests(test_path):
        try:
            unit = test_path.split(os.sep)[-1]
            cmd = ["make", "test", "-C", test_path]
            p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
        except OSError:
            ctx.fail(t(".could_not_run_tests", unit=unit))

        if p.returncode:
            logger.debug(pformat(cmd))
            logger.debug(pformat(out))
            logger.debug(pformat(err))
            ctx.fail(t(".tests_failed", unit=unit))

    def run_code_tests():
        code_path = os.path.join(path, "code")
        code_dist_path = os.path.join(code_path, "dist")
        if os.path.isdir(code_dist_path):
            shutil.rmtree(code_dist_path)

        run_tests(code_path)

    def run_codex_tests():
        codex_path = os.path.join(path, "codex")
        run_tests(codex_path)

    def create_code_tarball(code_params):
        code_path = os.path.join(path, "code")
        if not os.path.isdir(code_path):
            ctx.fail(t(".code_dir_not_exists"))

        code_dist_path = os.path.join(code_path, "dist")
        if os.path.isdir(code_dist_path):
            shutil.rmtree(code_dist_path)
        os.mkdir(code_dist_path)

        files_to_copy = [
            "readme.md", #FIXME add en
            "Makefile"
        ]
        files_to_copy.extend(code_params["exercise_files"])

        tarball = os.path.join(code_dist_path, "exercise.tar.gz")
        with closing(tarfile.open(tarball, "w:gz")) as tar:
            for file_rel_path in files_to_copy:
                tar.add(os.path.join(code_path, file_rel_path),
                        arcname=file_rel_path)

    def create_tarball():
        if os.path.isdir(dist_path):
            shutil.rmtree(dist_path)
        os.mkdir(dist_path)
        tarball = os.path.join(dist_path, tarball_name)

        exclude_files = [".+\.pyc$"]
        with closing(tarfile.open(tarball, "w:gz")) as tar:
            for (dirpath, dirnames, filenames) in os.walk(path):
                exclude_dirs = [
                    ".git",
                    "node_modules",
                    "bower_components",
                    "coverage",
                    ".tox"]
                dirnames[:] = [d for d in dirnames if d not in exclude_dirs]

                for filename in filenames:
                    if any(re.match(regexp, filename) for regexp in exclude_files):
                        continue
                    tar.add(os.path.join(dirpath, filename), arcname=os.path.join(dirpath.replace(path, ""), filename))
        return tarball

    upload_lesson()
    upload_lesson_version()


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
