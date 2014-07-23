
import importlib

from mhutils.fs.packages import PythonPackage

def test_can_import_all():
    print "Running test1"


    pkg = PythonPackage('/home/michael/dev/mreorg/src/mreorg')
    for modulename in pkg.module_names:

        try:
            i = importlib.import_module(modulename)
            print "Successfully imported:", modulename
        except:
            print "Error importing:", modulename



if __name__=='__main__':
    test_can_import_all()
