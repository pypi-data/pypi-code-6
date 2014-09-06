"""Give credit for the current git project or all projects down from cwd."""


from __future__ import division

import os
import sys
import time
import subprocess
from collections import Counter

from bladerunner.progressbar import ProgressBar

from git_credit import graph_output


class InsideGit(object):
    """Simple context manager to perform git actions inside the git dir."""

    def __init__(self, filepath):
        self.filepath = filepath
        self._prev_dir = os.getcwd()

    def __enter__(self, *args, **kwargs):
        os.chdir(self.filepath)

    def __exit__(self, *args, **kwargs):
        os.chdir(self._prev_dir)


def _clean_line(line):
    """Strips and maybe decodes a line of text."""

    line = line.strip()
    if isinstance(line, bytes):
        line = line.decode("latin-1")
    return line


def _run_cmd(cmd):
    """Runs a shell command and captures stdout."""

    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    output = []
    while True:
        try:
            stdout, _ = proc.communicate()
        except:
            break
        stdout = _clean_line(stdout)
        if stdout:
            output.append(stdout)
        time.sleep(.1)

    return "".join(output).splitlines()


def get_files_in_repo():
    """Get a list of git tracked python files in a repo (in the cwd)."""

    return _run_cmd("git ls-tree --name-only -r HEAD | grep -E '\\.py$'")


def get_credit(filepath):
    """Returns a Counter of {author: lines in HEAD} for a single file."""

    credit = Counter()
    cmd = "git blame --line-porcelain -L '/[^\\s]/' {0}".format(filepath)
    for line in _run_cmd(cmd):
        if not line.startswith("author "):
            continue

        author = line[7:]

        credit[author] += 1

    return credit


def is_git_dir(filepath):
    """Return a boolean of if this filepath has a .git folder."""

    git_dir = os.path.join(os.path.realpath(filepath), ".git")
    return os.path.exists(git_dir) and os.path.isdir(git_dir)


def sorted_by_value(credit):
    """Return the credit dict as a sorted list by value."""

    return sorted(credit.items(), key=lambda user: user[1], reverse=True)


def display_credit(credit):
    """Display the credit dict in a nice fashion."""

    total_per_committer = Counter()
    for repo, committers in credit.items():
        repo_total = sum(committers.values())
        title = "git credit for repo: {0}".format(repo)
        print(title)
        for committer, lines in sorted_by_value(committers):
            print("    {0}: {1} lines ({2:.1f}%)".format(
                committer,
                lines,
                ((lines / repo_total) * 100),
            ))

            total_per_committer[committer] += lines

    if len(credit) > 1:
        total_lines = sum(total_per_committer.values())
        title = "total git credit across all {0} repos:".format(len(credit))
        print(title)
        for committer, lines in sorted_by_value(total_per_committer):
            print("    {0}: {1} lines ({2:.1f}%)".format(
                committer,
                lines,
                ((lines / total_lines) * 100),
            ))

    return total_per_committer, title


def get_git_repos(filepath=None, existing_pbar=False):
    """Get a list of git repos down from filepath.

    Args::

        filepath: string filepath to search in
        existing_pbar: if a progressbar is already in progress
    """

    if filepath is None:
        filepath = os.curdir
    elif not os.path.exists(filepath):
        return []

    dirs = len([path for path in os.listdir(filepath) if os.path.isdir(path)])
    if dirs > 1 and not existing_pbar:
        pbar = ProgressBar(dirs, options={
            "left_padding": "finding repos ",
            "show_counters": True,
        })
        pbar.setup()
    else:
        pbar = None

    all_repos = []
    for repo, _, _ in os.walk(os.path.realpath(filepath)):
        if is_git_dir(repo) and not repo in all_repos:
            all_repos.append(repo)
            if pbar:
                pbar.update()

    if pbar:
        pbar.clear()

    return all_repos


def get_help(repo=None):
    """Raises SystemExit with a help message for the user."""

    if not repo:
        repo = [os.path.realpath(os.curdir)]

    if len(repo) == 1:
        msg = "{0} is not a git repo".format(repo[0])
    elif len(repo) == 2:
        msg = "Neither {0} nor {1} contain git repos".format(repo[0], repo[1])
    else:
        msg = "None of {0} or {1} contain git repos".format(
            ", ".join(repo[:-1]),
            repo[-1],
        )

    raise SystemExit(msg)


def get_all_git_repos(args):
    """Check for arguments as filepaths and build a list of repos with them."""

    pbar = None

    if len(args) == 1:
        all_repos = get_git_repos()
    elif len(args) == 2:
        all_repos = get_git_repos(args[1])
    else:
        all_repos = []
        all_args = args[1:]
        if len(all_args) > 1:
            pbar = ProgressBar(len(all_args), options={
                "left_padding": "finding repos ",
                "show_counters": True,
            })
            pbar.setup()

        for arg in all_args:
            for repo in get_git_repos(arg, True):
                if repo not in all_repos:
                    all_repos.append(repo)
                if pbar:
                    pbar.update()

    if pbar:
        pbar.clear()

    return all_repos or get_help(args[1:])


def get_all_tracked_files(all_repos):
    """For each repo, find all python files.

    Returns:
        a dictionary of {repo: [python files]}
    """

    # if we're doing multiple repos, inform the user that we're finding files
    num_repos = len(all_repos)
    if num_repos > 1:
        pbar = ProgressBar(num_repos, options={
            "left_padding": "finding tracked files ",
            "show_counters": True,
        })
        pbar.setup()
    else:
        pbar = None

    files_by_repo = {}
    for repo in all_repos:
        with InsideGit(repo):
            files_by_repo[repo] = get_files_in_repo()
            if pbar:
                pbar.update()

    if pbar:
        pbar.clear()

    return files_by_repo


def main():
    """Command line entry point."""

    pie_chart = False
    bar_chart = False

    args = sys.argv
    if "--pie" in args:
        pie_chart = True
        args.remove("--pie")
    elif "--bar" in args:
        bar_chart = True
        args.remove("--bar")

    # find repos and tracked files
    by_repo = get_all_tracked_files(get_all_git_repos(args))

    # get a count of all tracked files for the progress bar
    num_files = sum({_: len(files) for _, files in by_repo.items()}.values())
    pbar = ProgressBar(num_files, options={
        "left_padding": "getting credit per file ",
        "show_counters": True,
    })

    pbar.setup()
    all_credit = {}
    for repo, python_files in by_repo.items():
        with InsideGit(repo):
            repo_credit = Counter()

            for pyfile in python_files:
                repo_credit.update(get_credit(pyfile))
                pbar.update()

            all_credit[repo] = repo_credit

    pbar.clear()
    total_per_committer, graph_title = display_credit(all_credit)

    if pie_chart:
        graph_output.pie_chart(total_per_committer, graph_title)
    elif bar_chart:
        graph_output.bar_chart(total_per_committer, graph_title)


if __name__ == "__main__":
    main()
