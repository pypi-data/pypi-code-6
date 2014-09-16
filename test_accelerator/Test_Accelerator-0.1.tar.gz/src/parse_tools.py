
from fnmatch import fnmatch
import os
import re


def full_filenames(root, file_lst):
    """
    Creates a list of full file paths from
    the output of os.listdir

    :param root: the root of the files
    :param file_lst: list of file names
    :return: a list of the root joined to all the files
    """
    return [os.path.join(root, fn) for fn in file_lst]


def list_directory_files(directory, recursive, glob_pattern):
    """
    Lists the all of the file names in a directory

    :param directory: directory to search
    :param recursive: whether to recursively search directory
    :param glob_pattern: pattern to match files to. defaults to all files
    :return: a list of full path file names
    """
    if recursive:
        all_files = []
        for root, dirs, files in os.walk(directory):
            all_files += full_filenames(root, files)

    else:
        full_names = full_filenames(directory, os.listdir(directory))
        all_files = [fn for fn in full_names if os.path.isfile(fn)]

    relevant_files = filter(lambda filename: fnmatch(filename, glob_pattern), all_files)
    return relevant_files


def get_node_match(node, line_number, lines, strip):
    """
    Using a node checks if the line is a match.

    :param node: dict with lambda functions to test for a match
    :param line_number: the line number in the file
    :param lines: all the lines in the file from file.readlines()
    :param strip: bool whether to strip the line text
    :return: the match string, None if there is no match
    """
    do_strip = lambda text, flag: text.strip() if flag else text
    line = do_strip(lines[line_number], strip)
    initial_match = node['initial'](line)

    if initial_match and node.get('after'):
        if line_number+1 >= len(lines):
            return None
        next_line = do_strip(lines[line_number+1], strip)
        return node['after'](next_line)
    return initial_match


def node_search(search_files, node_lst, strip=True):

    """
    Generates full names of tests by iterating through
    files by finding matches with nodes. When it finds a match for the
    deepest node (leaf) it yields the match string and starts from the root.

    :param search_files:
    :param node_lst:
    :param strip:
    :return:
    """

    max_depth = len(node_lst)-1
    node_lst.sort(key=lambda node: node['depth'])
    running_name = '{}'

    for fn in search_files:
        cur_depth = 0
        with open(fn) as search_file:
            lines = search_file.readlines()
            for line_number, line in enumerate(lines):

                cur_node = node_lst[cur_depth]
                line = line.strip()

                node_match = get_node_match(cur_node, line_number, lines, strip)

                if node_match:
                    cur_name = node_match

                else:
                    match = None
                    for index in range(cur_depth):
                        # Check if the current line is a match of a earlier node.
                        match = get_node_match(node_lst[index], line_number, lines, strip)

                        if match:
                            cur_depth = index
                            cur_name = match
                            break

                    if not match:
                        continue

                if cur_depth == max_depth:
                    yield '{}.{}'.format(running_name, cur_name)

                else:
                    if cur_depth == 0:
                        running_name = node_match
                    else:
                        running_name = '{}.{}'.format(running_name, cur_name)

                    cur_depth = (cur_depth+1) % len(node_lst)



def print_test_names(agents, file_str, recursive, glob_pattern, node_list, strip, delimiter=','):
    """
    Since the best parallelization we can do is the number of jobs == number of agents;
    We print out the test in as many delimited chunks as there are agents.
    e.g. for 8 agents we print out 8 delimited strings

    :param agents: number of agents generating test names for
    :param file_str: comma separated string of directories and/or files
    :param recursive: bool whether to recursively search directories
    :param glob_pattern: pattern to match files
    :param node_list: list of node dicts
    :param strip: bool whether to strip the lines in files
    :param delimiter: the delimiter for the chunks
    :return: None
    """
    input_fn = file_str.split(',')
    file_names = []
    for fn in input_fn:
        if os.path.isdir(fn):
            file_names += list_directory_files(file_str, recursive, glob_pattern)
        else:
            file_names += fn

    names = [name for name in node_search(file_names, node_list, strip)]
    length = len(names)
    chunk_len = length/agents

    for i in range(1, agents+1):
        next = i*chunk_len
        if i == agents:
            next = max(length, next)
        print delimiter.join(names[i-1:next])


