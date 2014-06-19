__all__ = ["find", "find_and_delete"]
from hashlib import md5
import collections
import os
from mydupfilekiller.exceptions import *


def find(paths, output=False, skip_empty_files=True, follow_links=False):
    """
    A simple method to find all duplicate files.
    :param paths:  A list of paths.
    :type paths: list
    :param output: If True, it outputs the result to the console.
    :type output: bool
    :param skip_empty_files: It True, it skips empty files.
    :type skip_empty_files: bool
    :param follow_links: See https://docs.python.org/3/library/os.html#os.walk.
    :type follow_links: bool
    :return: A tuple of (file_num,dict). The dict is like {hash : (paths)}
    :rtype: tuple
    """
    hashes = collections.defaultdict(set)
    num = 0
    try:
        for path in paths:
            path = os.path.abspath(path)
            for root, dirs, files in os.walk(path, followlinks=follow_links):
                for name in files:
                    filename = os.path.join(root, name)
                    m = md5()
                    f = open(filename, 'rb')
                    buffer = 8192
                    while 1:
                        chunk = f.read(buffer)
                        if not chunk:
                            break
                        m.update(chunk)
                    f.close()
                    digest = m.hexdigest()
                    hashes[digest].add(filename)
                    num += 1
                    if output:
                        print("Processed %d files." % num)
        if skip_empty_files:
            m = md5()
            zero = m.hexdigest()
            if zero in hashes:
                del hashes[zero]
        if output:
            print("Done.")
            for key in hashes:
                set_ = hashes[key]
                if len(set_) > 1:
                    print("File hash: %s" % key)
                    for file in set_:
                        print(file)
                    print('')
    except SkipAllException:
        pass

    return num, hashes


def default_choose_callback(files):
    """
    Default choose callback. Ask the user to determine.
    :param files: A list of duplicate file paths.
    :type files: list
    :return: A set of subscripts to remove.
    :rtype: set
    """
    print('Choose files to delete [0-%d]:' % (len(files) - 1))
    num = 0
    for file in files:
        print('%d: %s' % (num, file))
        num += 1
    s = input("Input number to delete, separated by whitespace:")
    ret = set()
    numbers = s.split(" ")
    for num in numbers:
        if not (0 <= num <= len(files) - 1):
            continue
        ret.add(int(num))
    return ret


def find_and_delete(paths,
                    choose_callback=default_choose_callback,
                    output=False,
                    skip_empty_files=True,
                    follow_links=False):
    """
    Find the duplicate files and call choose_callback to delete files.
    :param paths: The paths to find.
    :type paths: list
    :param choose_callback: A callback like default_choose_callback, return files to delete.
    :type choose_callback: function
    :param output: If True, it outputs the result to the console.
    :type output: bool
    :param skip_empty_files: It True, it skips empty files.
    :type skip_empty_files: bool
    :param follow_links: See https://docs.python.org/3/library/os.html#os.walk.
    :type follow_links: bool
    :return: A tuple (files_deleted, bytes_freed).
    :rtype: tuple
    """
    files_deleted = list()
    bytes_freed = 0
    try:
        num, hashes = find(paths,
                           output,
                           skip_empty_files,
                           follow_links)
        files_deleted = list()
        bytes_freed = 0
        for key in hashes:
            set_ = hashes[key]
            if len(set_) > 1:
                files_to_remove = choose_callback(set_)
                for subscript in files_to_remove:
                    if not (0 <= subscript <= len(set_) - 1):
                        pass
                    files_deleted.append(set_[subscript])
                    bytes_freed += os.path.getsize(set_[subscript])
                    os.remove(set_[subscript])
        if output:
            print("Deleted %d files and freed %d bytes. Enjoy your free space!"
                  % (len(files_deleted), bytes_freed))
    except SkipAllException:
        pass
    return files_deleted, bytes_freed
