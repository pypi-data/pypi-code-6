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

@click.command(help="init lesson directory")
@click.argument('lesson_name')
@commands.shared_handling
def init(ctx, logger, t, lesson_name):
    cwd = os.getcwd()
    lesson_folder = "%s_lesson" % lesson_name
    if os.path.isdir(lesson_folder):
        ctx.fail(t(".folder_already_exists", folder=lesson_folder))
    else:
        shutil.copytree(hexlet.lesson_skeleton_path, lesson_folder)
        logger.info(t(".lesson_created", folder=lesson_folder))


@click.command()
@click.argument('hexlet_api_key')
@commands.shared_handling
def login(ctx, logger, t, hexlet_api_key):
    url = routes.api_teacher_check_auth_url(host=ctx.obj["host"], hexlet_api_key=hexlet_api_key)
    logger.debug(url)
    shared.login(ctx, logger, t, url, hexlet_api_key)


@click.command(help="submit lesson to server")
@click.argument("path", type=click.Path(exists=True, resolve_path=True))
@commands.shared_handling
def submit(ctx, logger, t, path):
    (name, kind) = os.path.split(path)[-1].rsplit("_", 1)
    if kind == "lesson":
        submit_lesson(ctx, logger, t, path, name)
    elif kind == "course":
        submit_course(ctx, logger, t, path, name)
    else:
        raise Exception()  # FIXME


def submit_course(ctx, logger, t, path, name):
    host = ctx.obj["host"]

    def upload_course():
        # FIXME check and submit lessons with order
        course_params = read_course_params()
        if len(course_params) > 0:
            files = {}
            payload = {"course": course_params}
            url = routes.api_teacher_courses_url(host=host)
            image_path = os.path.join(path, "assets", "main.jpg")

            logger.debug("Course url: '%s'" % url)

            if os.path.isfile(image_path):
                files["course[image]"] = open(image_path, 'rb')

            res = requests.post(
                url,
                data=utils.build_key_value(payload),
                files=files,
                timeout=1)
            if res.status_code == 201:
                logger.info(t(".course_uploaded", course=course_params["slug"]))
            else:
                ctx.fail(t(".course_upload_failure"))

    # read course if exists
    def read_course_params():
        # FIXME validate
        manifest_name = "course.yml"
        course_manifest_path = os.path.join(path, manifest_name)
        if os.path.isfile(course_manifest_path):
            with open(course_manifest_path, "r") as stream:
                data = yaml.load(stream)
                data["slug"] = name

                return data
        else:
            logger.debug(t(".course_not_found", path=course_manifest_path))
            return {}

    upload_course()


def submit_lesson(ctx, logger, t, path, name):
    host = ctx.obj["host"]
    tarball_name = "lesson.tar.gz"
    dist_path = os.path.join(path, "dist")

    def upload_lesson():
        lesson_params = read_lesson_params()

        payload = {
            "lesson": lesson_params
        }

        url = routes.api_teacher_lessons_url(host=host)
        headers = {'Content-Type': 'application/json'}
        res = requests.post(
            url,
            data=json.dumps(payload),
            headers=headers,
            timeout=1)
        if res.status_code == 201:
            logger.info(t(".lesson_uploaded", lesson=name))
        else:
            ctx.fail(t(".lesson_upload_failure"))

    def upload_lesson_version():
        lesson_params = read_lesson_params()

        if "code" in lesson_params["units"]:
            generate_code_dist()

        tarball_path = create_tarball()
        files = {"lesson_version[tarball]": open(tarball_path, 'rb')}
        url = routes.api_teacher_lesson_versions_url(name, host=host)
        res = requests.post(url, files=files, timeout=1)
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

    def generate_code_dist():
        code_params = read_code_params()
        run_code_tests()
        create_code_tarball(code_params)

    def run_code_tests():
        code_path = os.path.join(path, "code")
        code_dist_path = os.path.join(code_path, "dist")
        if os.path.isdir(code_dist_path):
            shutil.rmtree(code_dist_path)

        try:
            cmd = ["make", "test", "-C", code_path]
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
        except OSError:
            ctx.fail(t(".could_not_run_code_tests"))

        # FIXME !!!
        # if p.returncode:
        #     ctx.fail(t(".code_tests_failed"))

    def create_code_tarball(code_params):
        code_path = os.path.join(path, "code")
        if not os.path.isdir(code_path):
            ctx.fail(t(".code_dir_not_exists"))

        code_dist_path = os.path.join(code_path, "dist")
        if os.path.isdir(code_dist_path):
            shutil.rmtree(code_dist_path)
        os.mkdir(code_dist_path)

        files_to_copy = [
            "README.md",
            "Makefile"
        ]
        files_to_copy.extend(code_params["includes"])

        for file_rel_path in files_to_copy:
            src_file_path = os.path.join(code_path, file_rel_path)
            dst_file_path = os.path.join(code_dist_path, file_rel_path)
            dst_file_dir = os.path.dirname(dst_file_path)

            if not os.path.isdir(dst_file_dir):
                os.makedirs(dst_file_dir)

            if os.path.isfile(src_file_path):
                shutil.copy(src_file_path, dst_file_dir)
            else:
                ctx.fail(t(".code_file_not_exists", file=file_rel_path))

        tarball = os.path.join(code_dist_path, "exercise.tar.gz")
        with closing(tarfile.open(tarball, "w:gz")) as tar:
            for file_rel_path in files_to_copy:
                tar.add(os.path.join(code_dist_path, file_rel_path),
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
@click.option('--host', type=click.STRING, default=hexlet.host)
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
