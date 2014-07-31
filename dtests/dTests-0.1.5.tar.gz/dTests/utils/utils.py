from subprocess import call
import subprocess

def compile_file(file_name, lang):
    exit_code = 1
    if lang == "cpp":
        compile_name = ".".join(file_name.split(".")[:-1])
        exit_code = subprocess.call(["/usr/bin/env", "g++", file_name, "-o", compile_name])
    elif lang == "java":
        exit_code = subprocess.call(["/usr/bin/env", "javac", file_name])
    return exit_code == 0

def exec_file(file_name, lang, stdin=None):
    compile_name = ".".join(file_name.split(".")[:-1])
    output = ""
    
    if lang == "cpp":
        process = subprocess.Popen(["%s" % compile_name], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    elif lang == "java":
        process = subprocess.Popen(["/usr/bin/env", "java", compile_name], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    
    if stdin:
        process.stdin.write(stdin)
    process.stdin.close()
    process.wait()
    output = process.stdout.read()
    return output
