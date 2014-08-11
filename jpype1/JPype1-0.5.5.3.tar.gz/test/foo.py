import unittest
import jpype
import os.path as path

class PropertiesTestCase(unittest.TestCase):
    def setUp(self):
        if not jpype.isJVMStarted():
            root = path.dirname(path.abspath(path.dirname(__file__)))
            jvm_path = jpype.getDefaultJVMPath()
            print "Running testsuite using JVM", jvm_path
            classpath_arg = "-Djava.class.path=%s"
            classpath_arg %= '/home/marscher/sources/jpype/test/classes'
            jpype.startJVM(jvm_path, "-ea",
                           # "-Xcheck:jni", 
                           "-Xmx256M", "-Xms64M", classpath_arg)
        self.jpype = jpype.JPackage('jpype')
    
    def testprovokateBug(self):
        arr = jpype.JArray(jpype.JInt, 1)([1,2,3])
        p = self.jpype.properties.TestProp.factory(arr)
        
if __name__ == '__main__':
    unittest.main()
