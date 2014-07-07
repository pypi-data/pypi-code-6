import click
from click.testing import CliRunner

import conftest
import hexlet.commands.lesson as lesson

import os


def test_success_submit_lesson(monkeypatch):
    monkeypatch.setattr("requests.get", conftest.prepare_request_mock(status_code=200))
    monkeypatch.setattr("requests.post", conftest.prepare_request_mock(status_code=201))

    runner = CliRunner()
    #FIXME
    with runner.isolated_filesystem():
        args = ["submit", conftest.generate_fixture_path("algorithms_course/parallel_algorithms_lesson")]
        result = runner.invoke(lesson.cli, args)
        assert not result.exception
        assert result.output
        assert result.exit_code == 0


def test_success_submit_course(monkeypatch):
    monkeypatch.setattr("requests.get", conftest.prepare_request_mock(status_code=200))
    monkeypatch.setattr("requests.post", conftest.prepare_request_mock(status_code=201))

    runner = CliRunner()
    #FIXME
    with runner.isolated_filesystem():
        args = ["submit", conftest.generate_fixture_path("algorithms_course")]
        result = runner.invoke(lesson.cli, args)
        assert not result.exception
        assert result.output
        assert result.exit_code == 0


def test_failure_upload_course(monkeypatch, t):
    monkeypatch.setattr("requests.get", conftest.prepare_request_mock(status_code=200))
    monkeypatch.setattr("requests.post", conftest.prepare_lesson_submit_mock("upload_course"))

    runner = CliRunner()
    #FIXME
    with runner.isolated_filesystem():
        args = ["submit", conftest.generate_fixture_path("algorithms_course")]
        result = runner.invoke(lesson.cli, args)
        assert result.exception
        assert t("commands.lesson.submit.course_upload_failure") in result.output
        assert result.exit_code != 0


def test_failure_upload_lesson(monkeypatch, t):
    monkeypatch.setattr("requests.get", conftest.prepare_request_mock(status_code=200))
    monkeypatch.setattr("requests.post", conftest.prepare_lesson_submit_mock("upload_lesson"))

    runner = CliRunner()
    #FIXME
    with runner.isolated_filesystem():
        args = ["submit", conftest.generate_fixture_path("algorithms_course/parallel_algorithms_lesson")]
        result = runner.invoke(lesson.cli, args)
        assert result.exception
        assert t("commands.lesson.submit.lesson_upload_failure") in result.output
        assert result.exit_code != 0


def test_failure_upload_lesson_version(monkeypatch, t):
    monkeypatch.setattr("requests.get", conftest.prepare_request_mock(status_code=200))
    monkeypatch.setattr("requests.post", conftest.prepare_lesson_submit_mock("upload_lesson_version"))

    runner = CliRunner()
    #FIXME
    with runner.isolated_filesystem():
        args = ["submit", conftest.generate_fixture_path("algorithms_course/parallel_algorithms_lesson")]
        result = runner.invoke(lesson.cli, args=args)
        assert result.exception
        assert t("commands.lesson.submit.lesson_version_upload_failure") in result.output
        assert result.exit_code != 0


def test_no_lesson_manifest(monkeypatch, t):
    monkeypatch.setattr("requests.get", conftest.prepare_request_mock(status_code=200))
    monkeypatch.setattr("requests.post", conftest.prepare_lesson_submit_mock("upload_lesson_version"))

    runner = CliRunner()
    #FIXME
    with runner.isolated_filesystem():
        lesson_path = conftest.generate_fixture_path("algorithms_course/empty_lesson")
        args = ["submit", lesson_path]
        result = runner.invoke(lesson.cli, args)
        assert result.exception
        assert t("commands.lesson.submit.file_not_exists",
                  file="lesson.yml",
                  path=lesson_path) in result.output
        assert result.exit_code != 0

def test_exercise_upload(monkeypatch):
    monkeypatch.setattr("requests.get", conftest.prepare_request_mock(status_code=200))
    monkeypatch.setattr("requests.post", conftest.prepare_request_mock(status_code=201))

    runner = CliRunner()
    #FIXME
    with runner.isolated_filesystem():
        lesson_path = conftest.generate_fixture_path("http_course/http_base_lesson")
        args = ["submit", lesson_path]
        result = runner.invoke(lesson.cli, args)
        assert not result.exception
        assert result.output
        assert result.exit_code == 0
        assert os.path.isfile(os.path.join(lesson_path, "code", "dist", "exercise.tar.gz"))
