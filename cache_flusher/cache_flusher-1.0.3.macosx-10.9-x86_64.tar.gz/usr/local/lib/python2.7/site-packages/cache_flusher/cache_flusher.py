import platform
import os
import stat

def flush():
    OS = platform.system()

    if OS == "Windows" or OS.startswith("CYGWIN_NT"):
        dn = os.path.dirname(os.path.realpath(__file__))
        fn = os.path.join(dn, "data", "Flush.exe")
        st = os.stat(fn)

        if not st.st_mode & stat.S_IEXEC:
            os.chmod(fn, st.st_mode | stat.S_IEXEC)

        os.system('\"'+ fn + '\"')
    elif OS == "Darwin":
        os.system("purge")
    elif OS == "Linux":
        os.system("sync && echo 3 > /proc/sys/vm/drop_caches")
    else:
        print "Warning: Platform not supported"


if __name__ == "__main__":
    flush()
