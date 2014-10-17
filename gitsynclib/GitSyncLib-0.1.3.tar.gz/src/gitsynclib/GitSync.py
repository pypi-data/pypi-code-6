#!/usr/bin/env python

import os
import argparse
import yaml

from fabric.api import run, task, cd, hide, abort, settings, lcd, local, env, execute
from fabric.utils import puts
from fabric.contrib.files import exists
from fabric.colors import cyan

from GitNotified import GitNotified


class GitSync:

    local_path = ''
    local_branch = ''
    remote_path = ''
    remote_host = ''
    remote_user = ''
    git_ignore_lines = ''

    def __init__(self, config, notify):

        self.notify = notify

        self.local_path = os.path.expanduser(
            os.path.expandvars(config['local_path'])
        )
        self.local_branch = config['local_branch']
        self.remote_path = config['remote_path']
        self.remote_host = config['remote_host']
        self.remote_user = config['remote_user']

        if len(os.path.split(self.local_path)) < 2:
            abort(
                "The local path appears to be bad: {0}".format(self.local_path)
            )

        if 'git_ignore' in config:
            self.git_ignore_lines = config['git_ignore']
        else:
            self.git_ignore_lines = []

        # Sort the git ignore lines.
        self.git_ignore_lines = sorted(self.git_ignore_lines)

        if self.remote_user:
            self.remote_host = self.remote_user + '@' + self.remote_host

    @task
    def init_remote_master_repository(self, remote_path, local_branch, git_ignore_lines):

        puts("Setting up %s" % remote_path)

        if not exists(remote_path):
            abort("The remote path does not exist: %s" % remote_path)

        git_repo = self.get_remote_git_repo(self, remote_path)

        if exists(git_repo):
            puts("The git repo already exist: %s" % git_repo)
        else:
            with cd(remote_path):
                run("git init")

            self.update_git_ignore_file(self, remote_path, git_ignore_lines)

            with cd(remote_path):
                run("git add .gitignore")
                run("git commit -m 'Inital Commit'")
                run("git add .")
                run("git commit -m 'add project'")

    @task
    def update_git_ignore_file(self, remote_path, git_ignore_lines):

        puts("Updating ignore files.")

        with cd(remote_path):
            with hide('running'):

                cmd = []
                for line in git_ignore_lines:
                    cmd.append("echo '{0}' >> .gitignore_new".format(line))

                if cmd:
                    run(';'.join(cmd))
                    run('mv .gitignore_new .gitignore', shell=False)
                else:
                    run("echo '' > .gitignore")

    @task
    def remote_has_modified_files(self, remote_path):
        with cd(remote_path):
            with settings(warn_only=True):
                with hide('running', 'status', 'warnings', 'stderr', 'stdout'):

                    git_status_output = run("git status --porcelain .")

                    if not git_status_output:
                        puts(cyan("%s (remote) is clean." % remote_path))
                        return False
                    else:
                        puts(
                            cyan(
                                " %s (remote) has uncommitted changes."
                                % remote_path
                            )
                        )
                        return True

    @task
    def local_has_modified_files(self, local_path):
        with lcd(local_path):
            with settings(warn_only=True):
                with hide('running', 'status', 'warnings', 'stderr', 'stdout'):

                    git_status_output = local("git status --porcelain .", capture=True)

                    if not git_status_output:
                        puts(cyan("%s (local) is clean." % local_path))
                        return False
                    else:
                        puts(
                            cyan("%s (local) has uncommitted changes." % local_path)
                        )
                        return True

    @task
    def get_remote_git_repo(self, remote_path):
        git_repo = os.path.join(remote_path, '.git')
        return git_repo

    def check_local_path_case(self, path, full_path=None):
        if not full_path:
            full_path = path
        (head, tail) = os.path.split(path)
        if tail:
            self.check_local_path_case(head, full_path)

        if head == '/':
            return True

        if not os.path.isdir(head):
            return True

        if not os.path.exists(os.path.join(head, tail)):
            return True

        if tail not in os.listdir(head):
            abort(
                "Your local path appears to be miss configured, maybe the check"
                " to make sure upper and lower case letters are"
                " correct: {0}".format(full_path)
            )

    def check_local_path_permissions(self, path, full_path=None):
        if not full_path:
            full_path = path
        (head, tail) = os.path.split(path)
        if os.path.isdir(head):
            if not os.access(head, os.W_OK):
                abort(
                    (
                        "Unable to write to {0}, that means your local"
                        " path will not work. {1}"
                    ).format(head, full_path)
                )
        else:
            self.check_local_path_permissions(head, full_path)

    @task
    def get_local_git_clone(self, remote_path, local_path):
        self.check_local_path_case(local_path)
        self.check_local_path_permissions(local_path)

        local("git clone ssh://%s/%s %s" % (env.host, remote_path, local_path))

    @task
    def commit_remote_modified_files(self, remote_path):
        if not self.remote_has_modified_files(self, remote_path):
            return True
        with cd(remote_path):
            run("git add .")
            run("git commit -a -m 'committing all changes from %s'" % (remote_path))
            return True

    @task
    def push_remote_master(self, remote_path, local_branch):

        self.remote_has_local_branch(self, remote_path, local_branch)

        with cd(remote_path):
            run("git push origin %s" % (local_branch))
            return True

    def remote_has_local_branch(self, remote_path, local_branch):
        with cd(remote_path):
            git_branches = run('git branch')
            puts(cyan(git_branches))

    @task
    def pull_local(self, local_path):
        with lcd(local_path):
            local('git fetch origin')

    @task
    def merge_local_master(self, local_path):
        with lcd(local_path):
            local('git merge origin/master')

    @task
    def pull_and_merge_local(self, local_path):
        self.pull_local(self, local_path)
        self.merge_local_master(self, local_path)

    @task
    def commit_local_modified_files(self, local_path):
        with lcd(local_path):
            if self.local_has_modified_files(self, local_path):
                local("git add .")
                local(
                    "git commit -a -m 'committing all changes from a local machine'"
                )
        return True

    @task
    def push_local_to_remote(self, local_path, local_branch):
        if not self.local_has_local_branch(local_path, local_branch):
            self.local_create_local_branch(local_path, local_branch)

        with lcd(local_path):
            local("git push origin %s" % (local_branch))

    def local_create_local_branch(self, local_path, local_branch):
        with lcd(local_path):
            local('git branch %s' % (local_branch), capture=True)

    def local_has_local_branch(self, local_path, local_branch):

        puts(cyan(local_path))

        with lcd(local_path):
            git_branches = local('git branch', capture=True)
            for branch in git_branches.split():
                if branch == local_branch:
                    return True
            return False

    @task
    def merge_local_to_remote(self, remote_path, local_branch):
        with cd(remote_path):
            run('git merge %s' % (local_branch))

    @task
    def send_local_changes_to_remote(self, remote_path, local_path, local_branch):
        self.commit_local_modified_files(self, local_path)
        self.push_local_to_remote(self, local_path, local_branch)
        self.merge_local_to_remote(self, remote_path, local_branch)

    @task
    def send_remote_changes_to_local(self, remote_path, local_path):
        self.commit_remote_modified_files(self, remote_path)
        self.pull_and_merge_local(self, local_path)

    @task
    def sync(self, remote_path, local_path, local_branch, git_ignore_lines):

        if not os.path.exists(local_path):
            self.init(self, remote_path, local_path, local_branch, git_ignore_lines)

        if self.remote_has_modified_files(self, remote_path):
            self.send_remote_changes_to_local(self, remote_path, local_path)

        self.send_local_changes_to_remote(self, remote_path, local_path, local_branch)

    def initial_sync(self, remote_path, local_path, local_branch, git_ignore_lines):
        if not os.path.exists(local_path):
            self.init(self, remote_path, local_path, local_branch, git_ignore_lines)
        else:
            self.update_git_ignore_file(self, remote_path, git_ignore_lines)

        self.send_remote_changes_to_local(self, remote_path, local_path)
        self.send_local_changes_to_remote(self, remote_path, local_path, local_branch)

    @task
    def init(self, remote_path, local_path, local_branch, git_ignore_lines):
        self.init_remote_master_repository(self, remote_path, local_branch, git_ignore_lines)
        self.get_local_git_clone(self, remote_path, local_path)
        self.local_create_local_branch(local_path, local_branch)
        with lcd(local_path):
            local("git checkout %s" % (local_branch))

    def run_remote_has_modified_files(self):
        result = execute(
            self.remote_has_modified_files,
            self.remote_path,
            host=self.remote_host,
            remote_path=self.remote_path
        )
        return result[self.remote_host]

    def run_send_remote_changes_to_local(self):
        result = execute(
            self.send_remote_changes_to_local,
            self,
            host=self.remote_host,
            remote_path=self.remote_path,
            local_path=self.local_path
        )
        return result[self.remote_host]

    def run_send_local_changes_to_remote(self):
        result = execute(
            self.send_local_changes_to_remote,
            self,
            host=self.remote_host,
            remote_path=self.remote_path,
            local_path=self.local_path,
            local_branch=self.local_branch
        )
        return result[self.remote_host]

    def run_initial_sync(self):
        self.notify.sync_start(self.local_path, self.remote_path, self.remote_host)
        execute(
            self.initial_sync,
            host=self.remote_host,
            remote_path=self.remote_path,
            local_path=self.local_path,
            local_branch=self.local_branch,
            git_ignore_lines=self.git_ignore_lines
        )
        self.notify.sync_done(self.local_path, self.remote_path, self.remote_host)

    def run_sync(self):

        self.notify.sync_start(self.local_path, self.remote_path, self.remote_host)

        try:
            if self.run_remote_has_modified_files():
                self.run_send_remote_changes_to_local()

            self.run_send_local_changes_to_remote()
        except Exception as e:
            print("sync failed.")
            print(type(e))
            print(e.args)
            print(e)
            self.notify.sync_failed()
            raise
        else:
            self.notify.sync_done(self.local_path, self.remote_path, self.remote_host)


def parse_config():
    # Setup Parser
    parser = argparse.ArgumentParser(
        description='Use git to sync a site on a server to your local machine.'
    )

    parser.add_argument(
        'config_file',
        nargs='?',
        type=argparse.FileType('r')
    )

    parser.add_argument(
        'command',
        nargs='?',
        type=str
    )

    args = parser.parse_args()

    # Read in config file.
    return yaml.safe_load(args.config_file)


def main():

    parser = argparse.ArgumentParser(
        description='Use git to sync a site on a server to your local machine.'
    )

    parser.add_argument(
        'config_file',
        nargs='?',
        type=argparse.FileType('r')
    )

    parser.add_argument(
        'command',
        nargs='?',
        type=str
    )

    args = parser.parse_args()

    config = yaml.safe_load(args.config_file)

    notifier = GitNotified()

    git_sync = GitSync(config, notifier)

    if args.command == "init":
        git_sync.run_initial_sync()
    elif args.command == 'sync':
        git_sync.run_sync()
    else:
        notifier.notify("Invalid command.")

    return 0

if __name__ == '__main__':
    main()
