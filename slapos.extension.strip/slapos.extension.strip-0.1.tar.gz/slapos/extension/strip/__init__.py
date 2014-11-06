import os
import re
import stat
import subprocess

def finish(buildout):
    print 'Stripping binaries ...'
    buildout_directory = buildout['buildout']['directory']
    file_binary = buildout['buildout'].get('file-binary', 'file')
    find_binary = buildout['buildout'].get('find-binary', 'find')
    strip_binary = buildout['buildout'].get('strip-binary', 'strip')

    def run_strip(path, strip_args):
        mode = os.stat(path).st_mode
        writable_mode = mode | stat.S_IWUSR
        if mode != writable_mode:
            os.chmod(path, writable_mode)
        args = [strip_binary,] + strip_args + [path,]
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        result, _ = p.communicate()
        if mode != writable_mode:
            os.chmod(path, mode)

    # Same logic as Debian's dh_strip script.
    args = [find_binary, buildout_directory, '-type', 'f']
    try:
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        file_list, _ = p.communicate()
        shared_lib_list = []
        executable_list = []
        static_lib_list = []
        for path in file_list.splitlines():
            file_name = os.path.basename(path)
            if re.match('.*\.(so(\..+)?|cmxs)$', file_name):
                args = [file_binary, path]
                p = subprocess.Popen(args, stdout=subprocess.PIPE)
                result, _ = p.communicate()
                if re.match('.*ELF.*shared.*not stripped', result):
                    shared_lib_list.append(path)
            elif os.stat(path).st_mode & stat.S_IEXEC:
                args = [file_binary, path]
                p = subprocess.Popen(args, stdout=subprocess.PIPE)
                result, _ = p.communicate()
                if re.match('.*ELF.*(executable|shared).* not stripped', result):
                    executable_list.append(path)
            elif re.match('lib.*\.a$', file_name):
                static_lib_list.append(path)
        for path in shared_lib_list:
            strip_args = [
                '--remove-section=.comment',
                '--remove-section=.note',
                '--strip-unneeded',
            ]
            run_strip(path, strip_args)
        for path in executable_list:
            strip_args = [
                '--remove-section=.comment',
                '--remove-section=.note',
            ]
            run_strip(path, strip_args)
        for path in shared_lib_list:
            strip_args = [
                '--strip-debug',
            ]
            run_strip(path, strip_args)
        print 'Done.'
    except OSError, e:
        print 'Command failed: %s: %s' % (e, args)
