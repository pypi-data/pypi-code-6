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

def clean_branch(branch):
    b = []
    for key,value in branch.iteritems():
        if isinstance(value,str):
            b.append(key)
        else:
            b.append({key:clean_branch(value)})
    return b

def raw_tree(git_dir,commit_sha):
    commit_tree = tree(git_dir,commit_sha)
    return clean_branch(commit_tree)

def array_branch(branch,relative_path=None):
    b = []
    for key,value in branch.iteritems():
        if relative_path is None:
            path = key
        else:
            path = os.path.join(relative_path,key)
        if isinstance(value,str):
            f = {
                "isDir":False,
                "name":key,
                "path":path
            }
        else:
            f = {
                "isDir":True,
                "name":key,
                "path":path,
                "files":array_branch(value,path)
            }
        b.append(f)
    return b

def array_tree(git_dir,commit_sha):
    commit_tree = tree(git_dir,commit_sha)
    return array_branch(commit_tree)

def bundle_branch(branch,zf,git_dir,relative_path=None):
    for key,value in branch.iteritems():
        if relative_path is None:
            path = key
        else:
            path = os.path.join(relative_path,key)
        if isinstance(value,str):
            info = zipfile.ZipInfo(path)
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info,_cat_file(git_dir,value))
        else:
            bundle_branch(value,zf,git_dir,path)

def bundle(git_dir,commit_sha):
    commit_tree = tree(git_dir,commit_sha)
    if len(commit_sha) > 8:
        commit_sha = commit_sha[:8]
    zipname = "%s.zip" % commit_sha
    zf = zipfile.ZipFile(zipname,"w")
    bundle_branch(commit_tree,zf,git_dir,commit_sha)
    zf.close()
    return zipname

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

