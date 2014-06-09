from hashlib import md5
import collections
import sys
import os


def find(paths, output=False):
    """
    A simple method to find all duplicate files.
    :param paths:  A list of paths.
    :param output: If True, it outputs the result to the console.
    :return: A tuple of (file_num,dict). The dict is like {hash : [files]}
    """
    hashes = collections.defaultdict(list)
    num = 0
    for path in paths:
        for root, dirs, files in os.walk(path):
            for name in files:
                filename = os.path.abspath(os.path.join(root, name))
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
                hashes[digest].append(filename)
                num += 1
                if output:
                    print("Processed %d files." % num)
    if output:
        print("Done.")
        for key in hashes:
            _list = hashes[key]
            if len(_list) > 1:
                print("File hash: ", key)
                for file in _list:
                    print(file)
                print('')
    return num, hashes


def default_choose_callback(files):
    """
    Default choose callback. Ask the user to determine.
    :param files: A list of duplicate file paths.
    :return: A list of files to remove.
    """
    print('Choose files to delete [0-%d]:' % (len(files)-1))
    num = 0
    for file in files:
        print('%d: %s' % (num, file))
        num += 1
    s = input("Input number to delete, separated by whitespace:")
    ret = set()
    numbers = s.split(" ")
    for num in numbers:
        if not num in range(0,len(files)):
            pass
        ret.add(int(num))
    return list(ret)


def find_and_delete(paths, choose_callback=default_choose_callback, output=False):
    """
    Find the duplicate files in paths and call choose_callback to determine which to remove.
    :param paths: The paths to find.
    :param choose_callback: A callback like choose_callback([paths]) and returns a list of subscripts.
    :param output: If True, it outputs the result to the console.
    :return: A tuple (files_deleted, bytes_freed).
    """
    num, hashes = find(paths, output)
    files_deleted = list()
    bytes_freed = 0
    for key in hashes:
        _list = hashes[key]
        if len(_list) > 1:
            files_to_remove = choose_callback(_list)
            for subscript in files_to_remove:
                files_deleted.append(_list[subscript])
                bytes_freed += os.path.getsize(_list[subscript])
                os.remove(_list[subscript])
    if output:
        print("Deleted %d files and freed %d bytes. Enjoy your free space!" % (len(files_deleted), bytes_freed))
    return files_deleted, bytes_freed


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("You need to specify at least one path.")
        sys.exit()
    find_and_delete(sys.argv[1:], default_choose_callback, True)
