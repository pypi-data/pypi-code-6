from __future__ import print_function

import json
import os
import os.path
import subprocess as sp
import sys
import zipfile

def _cat_file(git_dir,sha):
    return sp.check_output(["git", 
                            "--git-dir",git_dir,
                            "cat-file","-p",sha])

def _crawl_tree(git_dir,tree_sha):
    dir_content = {}
    tree_content = _cat_file(git_dir,tree_sha).strip()
    for line in tree_content.split("\n"):
        _,file_type,file_sha,filename = line.split()
        if file_type == "tree":
            dir_content[filename] =_crawl_tree(git_dir,file_sha)
        elif file_type == "blob":
            dir_content[filename] = file_sha
    return dir_content

def tree(git_dir,commit_sha):
    if len(commit_sha) > 8:
        commit_sha = commit_sha[:8]
    commit_content = _cat_file(git_dir,commit_sha)
    tree_sha = commit_content.split("\n")[0].split()[1]
    return _crawl_tree(git_dir,tree_sha)

def cat(git_dir,commit_sha,filepath):
    commit_tree = tree(git_dir,commit_sha)
    filepath = filepath.split(os.sep)
    try:
        for path in filepath:
            commit_tree = commit_tree[path]
    except KeyError:
        raise Exception("No file named: %s" % filepath)
    sha = commit_tree
    if not isinstance(sha,str):
        raise Exception("Cannot cat a directory")
    return _cat_file(git_dir,sha)


if __name__ == "__main__":
    git_dir = sys.argv[1]
    sha = sys.argv[2]
    git_archive(git_dir,sha)

