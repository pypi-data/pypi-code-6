import os.path, distutils.sysconfig
from distutils.core import setup
txt="cls\nset pyPath=import pyInstalls; pyInstalls.quickInstaller(r'%1')\npython  -c \"%pyPath%\" \ncmd" 
#install using python setup.py sdist, put this and it's module in the same folder

#setup info
setup(
        name='pyInstalls',
        version='1.0',
        py_modules=['pyInstalls'],
        license = "BSD",      
        platforms = ["Windows"],        
        author = "Ryan Beall",        
        author_email = "bealldev@gmail.com"
        )
        
#get python install folder
installFolder= distutils.sysconfig.get_python_lib()


#if there's one it can find
if installFolder:    
    
    #send to folder, where your bat file will live
    destination=os.path.expanduser("~\AppData\Roaming\Microsoft\Windows\SendTo")
    
    #bat file destination
    name = os.path.abspath(destination +"\\installer.cmd")
    
    #make that bat file son
    with open(name, "w") as cmd_file:    
        cmd_file.write(txt)