# coding: utf-8
"""
File ID: 3xzSy5a
"""

import os
import sys

def find_executable(prog):
    """
    Find paths of the executable specified by |prog|.
    
    #/ |prog| can be either name or path
    aoikww notepad.exe
    aoikww C:\Windows\notepad.exe
    
    #/ |prog| can be either absolute or relative
    aoikww C:\Windows\notepad.exe
    aoikww Windows\notepad.exe
    
    #/ |prog| can be either with or without extension
    aoikww notepad.exe
    aoikww notepad
    aoikww C:\Windows\notepad.exe
    aoikww C:\Windows\notepad
    """
    #/
    exe_path_s = []

    #/ 8f1kRCu
    env_var_PATHEXT = os.environ.get('PATHEXT', None)
    
    #/ 6qhHTHF
    #/ split into a list of extensions
    if env_var_PATHEXT is None:
        ext_s = []
    else:
        ext_s = env_var_PATHEXT.split(os.pathsep)
        ## |os.pathsep| on Windows is |;|
    
    #/ 2pGJrMW 
    #/ strip
    ext_s = [x.strip() for x in ext_s]
    
    #/ 2gqeHHl
    #/ remove empty
    ext_s = [x for x in ext_s if x != '']
    
    #/ 2zdGM8W
    #/ convert to lowercase
    ext_s = [x.lower() for x in ext_s]
    
    #/ 2fT8aRB
    #/ uniquify
    ext_s_unique = []
    
    for ext in ext_s:
        if ext not in ext_s_unique:
            ext_s_unique.append(ext)
            
    ext_s = ext_s_unique
    del ext_s_unique
    
    #/ convert |ext_s| to a tuple
    ## Becasue |string.endswith| below takes tuple as argument, not list.
    ## Used at 6kZa5cq.
    ext_st = tuple(ext_s)

    #/ 4ysaQVN
    env_var_PATH = os.environ.get('PATH', None)

    #/ 6mPI0lg
    if env_var_PATH is None:
        dir_path_s = []
    else:
        dir_path_s = env_var_PATH.split(os.pathsep)
        ## |os.pathsep| on Windows is |;|
    
    #/ 5rT49zI
    #/ insert empty dir path to the beginning
    ##
    ## Empty dir handles the case that |prog| is a path, either relative or absolute.
    ## See code 7rO7NIN.
    if '' not in dir_path_s:
       dir_path_s.insert(0, '')
    
    #/ 2klTv20
    #/ uniquify
    dir_path_s_unique = []
    
    for dir_path in dir_path_s:
        if dir_path not in dir_path_s_unique:
            dir_path_s_unique.append(dir_path)
    
    #/ 6bFwhbv
    for dir_path in dir_path_s_unique:
        #/ 7rO7NIN
        #/ synthesize a path with the dir and prog
        path = os.path.join(dir_path, prog)
        
        #/ 6kZa5cq
        ## assume the path has extension, check if it is an executable
        if os.path.isfile(path) and path.endswith(ext_st):
            exe_path_s.append(path)

        #/ 2sJhhEV
        ## assume the path has no extension
        for ext in ext_s:
            #/ 6k9X6GP
            #/ synthesize a new path with the path and the executable extension
            path_plus_ext = path + ext
            
            #/ 6kabzQg
            #/ check if it is an executable
            if os.path.isfile(path_plus_ext):
                exe_path_s.append(path_plus_ext)
    
    #/ 8swW6Av
    #/ uniquify
    exe_path_s_unique = []
    
    for exe_path in exe_path_s:
        if exe_path not in exe_path_s_unique:
            exe_path_s_unique.append(exe_path)

    #/
    return exe_path_s_unique

def main():
    #/ 9mlJlKg
    #/ check if one cmd arg is given
    ## I was using |argparse| module to parse the arguments, which was very
    ## convenient. However, |argparse| module is not available until python
    ## version 2.7 and 3.2. So here I simply check the number of arguments
    ## given instead.
    if len(sys.argv) != 2:
        #/ 7rOUXFo
        #/ print program usage
        print(r'Usage: aoikww PROG')
        print('')
        print(r'#/ PROG can be either name or path')
        print(r'aoikww notepad.exe')
        print(r'aoikww C:\Windows\notepad.exe')
        print('')
        print(r'#/ PROG can be either absolute or relative')
        print(r'aoikww C:\Windows\notepad.exe')
        print(r'aoikww Windows\notepad.exe')
        print('')
        print(r'#/ PROG can be either with or without extension')
        print(r'aoikww notepad.exe')
        print(r'aoikww notepad')
        print(r'aoikww C:\Windows\notepad.exe')
        print(r'aoikww C:\Windows\notepad')
        
        #/ 3nqHnP7
        return

    #/ 9m5B08H
    #/ get name or path of a program from cmd arg
    prog = sys.argv[1]
    
    #/ 8ulvPXM
    #/ find executables
    path_s = find_executable(prog)
    
    #/ 5fWrcaF
    #/ has found none, exit
    if not path_s:
        #/ 3uswpx0
        return
    
    #/ 9xPCWuS
    #/ has found some, output
    txt = '\n'.join(path_s)
    
    print(txt)
    
    #/ 4s1yY1b
    return

if __name__ == '__main__':
    main()
    