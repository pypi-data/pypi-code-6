import jpype
jvm_path = jpype.getDefaultJVMPath()
jpype.startJVM(jpype.getDefaultJVMPath(), '-Xmx256M', '-Xms64M', '-Djava.class.path=/home/marscher/sources/jpype/test/classes')
assert jpype.isJVMStarted()
cls = jpype.JPackage('jpype').io.ExceptionWhileIO('pickled_list.bin')
cls.read()
