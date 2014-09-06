"""Unit tests for git_credit.base."""


from __future__ import division

import os
import sys
import pytest
from mock import Mock, patch

from git_credit import base


@pytest.fixture(params=(
        ["fname"],
        ["fname", "/fake/dir/not/real"],
        ["fname", "/fake/dir/not/real", "/totes/fake/not/even/real"],
        ["fname", "/fake/dir", "/not/real", "/totes/fake/dir", "/cant/even/"],
    ),
    ids=("no dirs", "one dir", "two dirs", "many dirs"),
)
def args(request):
    return request.param


def test_parse_args(args):
    """Check the lazy arg parser is working as intended."""

    with patch.object(base, "get_git_repos", return_value=["fake"]) as mockgit:
        base.get_all_git_repos(args)

    for arg in args[1:]:
        if len(args[1:]) > 1:
            mockgit.assert_any_call(arg, True)
        else:
            mockgit.assert_any_call(arg)

    assert mockgit.called


def test_getting_help(args):
    """Ensure the error message is raised."""

    args = args[1:]
    with pytest.raises(SystemExit) as sys_exit:
        base.get_help(args)

    if not args:
        exp = "{0} is not a git repo".format(os.path.realpath(os.curdir))
    elif len(args) == 1:
        exp = "{0} is not a git repo".format(args[0])
    elif len(args) == 2:
        exp = "Neither {0} nor {1} contain git repos".format(args[0], args[1])
    else:
        exp = "None of {0} or {1} contain git repos".format(
            ", ".join(args[:-1]),
            args[-1],
        )

    assert exp in sys_exit.value.args


def test_main():
    """Mock to ensure program flow."""

    with patch.object(base, "get_all_git_repos") as mock_parse:
        with patch.object(base, "display_credit", return_value=(0, 1)) as disp:
            base.main()
    mock_parse.assert_called_once_with(sys.argv)
    assert disp.called


@pytest.mark.parametrize("filepath", (".", "..", None, "/fake/dir"))
def test_get_git_repos(filepath):
    """A whole lot of mocking going on here..."""

    exists_mock = patch.object(base.os.path, "exists", return_value=True)
    isdir_mock = patch.object(base.os.path, "isdir", return_value=True)
    listdir_mock = patch.object(base.os, "listdir", return_value=["ok"])
    realpath_mock = patch.object(base.os.path, "realpath", return_value="fake")
    walk_mock = patch.object(base.os, "walk", return_value=[("ok", 0, 0)])
    git_dir_mock = patch.object(base, "is_git_dir", return_value=True)

    with exists_mock:
        with isdir_mock:
            with listdir_mock:
                with realpath_mock as mock_realpath:
                    with walk_mock as mock_walk:
                        with git_dir_mock as mock_git_dir:
                            assert base.get_git_repos(filepath) == ["ok"]

    if filepath is None:
        mock_realpath.assert_called_once_with(os.curdir)
    else:
        mock_realpath.assert_called_once_with(filepath)

    mock_walk.assert_called_once_with("fake")
    mock_git_dir.assert_called_once_with("ok")


@pytest.mark.parametrize("test_input",
    (
        {"fake_repo": {"johann": 30, "julia": 40, "cornelia": 30}},
        {
            "fake_repo": {"vilda": 25, "melvin": 40, "melissa": 35},
            "other_repo": {"jessica": 60, "daniel": 40},
        },
        {
            "fake_repo": {"vilda": 25, "melvin": 40, "melissa": 35},
            "other_repo": {"jessica": 60, "daniel": 40},
            "repo_trio": {"melvin": 90, "fernado": 10},
        }
    ),
    ids=("one", "more than one", "same person different repo"),
)
def test_output_more_than_one(test_input, capfd):
    """Test the output formatting with fake data."""

    base.display_credit(test_input)
    out, _ = capfd.readouterr()
    out = out.splitlines()

    all_committers = {}
    for repo, committers in test_input.items():
        repo_lines = sum(committers.values())
        assert "git credit for repo: {0}".format(repo) in out
        for name, lines in committers.items():
            assert "    {0}: {1} lines ({2:.1f}%)".format(
                name,
                lines,
                ((lines / repo_lines) * 100),
            ) in out
            if name in all_committers:
                all_committers[name] += lines
            else:
                all_committers[name] = lines

    if len(test_input) > 1:
        exp = "total git credit across all {0} repos:".format(len(test_input))
        assert exp in out
        total_lines = sum(all_committers.values())
        for name, lines in all_committers.items():
            assert "    {0}: {1} lines ({2:.1f}%)".format(
                name,
                lines,
                ((lines / total_lines) * 100),
            ) in out


def test_is_git_dir():
    """Mock all calls to test determining if we are in a git dir."""

    realpath_mock = patch.object(base.os.path, "realpath", return_value="ok")
    join_mock = patch.object(base.os.path, "join", return_value="joined")

    with realpath_mock as mock_realpath:
        with join_mock as mock_join:
            with patch.object(base.os.path, "exists") as mock_exists:
                with patch.object(base.os.path, "isdir") as mock_isdir:
                    base.is_git_dir("something")

    mock_realpath.assert_called_once_with("something")
    mock_join.assert_called_once_with("ok", ".git")
    mock_exists.assert_called_once_with("joined")
    mock_isdir.assert_called_once_with("joined")
