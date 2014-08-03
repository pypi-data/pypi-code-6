def built(name_setup, version, description, name_py):
    
    """The "name_setup" is what does your moduel's name,

       next "version" just your coding's version,

       and then "description" is its mean,
       
       finally "name_py" of index is that you want to bulit file.py."""
    
    #PS. All index must add <""> or <''> in their left and right side.
    
    try:
        with open('setup.py', 'w')as f:
            print('import sys\nfrom cx_Freeze import setup, Executable\n# Dependencies are automatically detected, but it might need fine tuning.\nbuild_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}\n# GUI applications require a different base on Windows (the default is for a\n# console application).\nbase = None\nif sys.platform == "win32":\n\tbase = "Win32GUI"\nsetup(  name = '+'"'+name_setup+'"'+',\n\tversion = "'+version+'",\n\tdescription = '+'"'+description+'"'+',\n\toptions = {"build_exe": build_exe_options},\n\texecutables = [Executable('+'"'+name_py+'"'+', base=base)])', file=f)
    except IOError as ioerr:
                  print("File error :"+ str(ioerr))
