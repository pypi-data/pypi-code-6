Python 3.3.5 (v3.3.5:62cf4e77f785, Mar  9 2014, 10:35:05) [MSC v.1600 64 bit (AMD64)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> pr
Traceback (most recent call last):
  File "<pyshell#0>", line 1, in <module>
    pr
NameError: name 'pr' is not defined
>>> print
<built-in function print>
>>> members=[cf,wyz,yjl,zwx]
Traceback (most recent call last):
  File "<pyshell#2>", line 1, in <module>
    members=[cf,wyz,yjl,zwx]
NameError: name 'cf' is not defined
>>> members=["cf","wyz","yjl","zwx"]
>>> print(members)
['cf', 'wyz', 'yjl', 'zwx']
>>> append("gx")
Traceback (most recent call last):
  File "<pyshell#5>", line 1, in <module>
    append("gx")
NameError: name 'append' is not defined
>>> members.append("gx")
>>> print(members[3])
zwx
>>> members.extend(["zcx",4])
>>> print(mem)
Traceback (most recent call last):
  File "<pyshell#9>", line 1, in <module>
    print(mem)
NameError: name 'mem' is not defined
>>> print
<built-in function print>
>>> print(members)
['cf', 'wyz', 'yjl', 'zwx', 'gx', 'zcx', 4]
>>> members.pop()
4
>>> print(members)
['cf', 'wyz', 'yjl', 'zwx', 'gx', 'zcx']
>>> members.insert(1,cal)
Traceback (most recent call last):
  File "<pyshell#14>", line 1, in <module>
    members.insert(1,cal)
NameError: name 'cal' is not defined
>>> members.insert(1,"cal")
>>> members.remove("gx")
>>> print(members)
['cf', 'cal', 'wyz', 'yjl', 'zwx', 'zcx']
>>> members.append('"str"')
>>> print(members)
['cf', 'cal', 'wyz', 'yjl', 'zwx', 'zcx', '"str"']
>>> members.insert(7,"\"test\"|)
	       
SyntaxError: EOL while scanning string literal
>>> members.insert(7,"\"test\""))
SyntaxError: invalid syntax
>>> members.insert(7,"\"test\"")
>>> print(members)
['cf', 'cal', 'wyz', 'yjl', 'zwx', 'zcx', '"str"', '"test"']
>>> for name in members:
	print(name)
	;
	
SyntaxError: invalid syntax
>>> for name in members:
	print(name)

	
cf
cal
wyz
yjl
zwx
zcx
"str"
"test"
>>> dir(_buitins_)
Traceback (most recent call last):
  File "<pyshell#30>", line 1, in <module>
    dir(_buitins_)
NameError: name '_buitins_' is not defined
>>> dir(_builtins_)
Traceback (most recent call last):
  File "<pyshell#31>", line 1, in <module>
    dir(_builtins_)
NameError: name '_builtins_' is not defined
>>> dir(_buildins_)
Traceback (most recent call last):
  File "<pyshell#32>", line 1, in <module>
    dir(_buildins_)
NameError: name '_buildins_' is not defined
>>> dir(__builtins__)
['ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BlockingIOError', 'BrokenPipeError', 'BufferError', 'BytesWarning', 'ChildProcessError', 'ConnectionAbortedError', 'ConnectionError', 'ConnectionRefusedError', 'ConnectionResetError', 'DeprecationWarning', 'EOFError', 'Ellipsis', 'EnvironmentError', 'Exception', 'False', 'FileExistsError', 'FileNotFoundError', 'FloatingPointError', 'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning', 'IndentationError', 'IndexError', 'InterruptedError', 'IsADirectoryError', 'KeyError', 'KeyboardInterrupt', 'LookupError', 'MemoryError', 'NameError', 'None', 'NotADirectoryError', 'NotImplemented', 'NotImplementedError', 'OSError', 'OverflowError', 'PendingDeprecationWarning', 'PermissionError', 'ProcessLookupError', 'ReferenceError', 'ResourceWarning', 'RuntimeError', 'RuntimeWarning', 'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError', 'TimeoutError', 'True', 'TypeError', 'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning', 'ValueError', 'Warning', 'WindowsError', 'ZeroDivisionError', '_', '__build_class__', '__debug__', '__doc__', '__import__', '__loader__', '__name__', '__package__', 'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'compile', 'complex', 'copyright', 'credits', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'exit', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'license', 'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'quit', 'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip']
>>> members.pop()
'"test"'
>>> print(members)
['cf', 'cal', 'wyz', 'yjl', 'zwx', 'zcx', '"str"']
>>> members.remove(5)
Traceback (most recent call last):
  File "<pyshell#36>", line 1, in <module>
    members.remove(5)
ValueError: list.remove(x): x not in list
>>> members.remove('zcx')
>>> members.reverse()
>>> print(members)
['"str"', 'zwx', 'yjl', 'wyz', 'cal', 'cf']
>>> members.remove('str')
Traceback (most recent call last):
  File "<pyshell#40>", line 1, in <module>
    members.remove('str')
ValueError: list.remove(x): x not in list
>>> members.remove('"str"')
>>> print(members)
['zwx', 'yjl', 'wyz', 'cal', 'cf']
>>> members.append(["male",20])
>>> print(members)
['zwx', 'yjl', 'wyz', 'cal', 'cf', ['male', 20]]
>>> for member in members:
	if isinstance(member,list)
	
SyntaxError: invalid syntax
>>> for member in members:
	if isinstance(member,list):
		for nested_mem in member:
			print(nested_mem)
	else:
		print(member)

		
zwx
yjl
wyz
cal
cf
male
20
>>> members[5].append(['180cm','60kg'])
>>> print(members)
['zwx', 'yjl', 'wyz', 'cal', 'cf', ['male', 20, ['180cm', '60kg']]]
>>> def print_lol(alist):
	for item in alist:
		if isinstance(item,list):
			print(item)
		else:
			print(alist)

			
>>> print_lol(members)
['zwx', 'yjl', 'wyz', 'cal', 'cf', ['male', 20, ['180cm', '60kg']]]
['zwx', 'yjl', 'wyz', 'cal', 'cf', ['male', 20, ['180cm', '60kg']]]
['zwx', 'yjl', 'wyz', 'cal', 'cf', ['male', 20, ['180cm', '60kg']]]
['zwx', 'yjl', 'wyz', 'cal', 'cf', ['male', 20, ['180cm', '60kg']]]
['zwx', 'yjl', 'wyz', 'cal', 'cf', ['male', 20, ['180cm', '60kg']]]
['male', 20, ['180cm', '60kg']]
>>> def pirnt_lol(the_list):
	for item in the_list:
		if isinstance(item,list):
			print_lol(item)
		else:
			print(item)

			
>>> print_lol(members)
['zwx', 'yjl', 'wyz', 'cal', 'cf', ['male', 20, ['180cm', '60kg']]]
['zwx', 'yjl', 'wyz', 'cal', 'cf', ['male', 20, ['180cm', '60kg']]]
['zwx', 'yjl', 'wyz', 'cal', 'cf', ['male', 20, ['180cm', '60kg']]]
['zwx', 'yjl', 'wyz', 'cal', 'cf', ['male', 20, ['180cm', '60kg']]]
['zwx', 'yjl', 'wyz', 'cal', 'cf', ['male', 20, ['180cm', '60kg']]]
['male', 20, ['180cm', '60kg']]
>>> def print2(a_list):
	for item in a_list:
		if isinstance(item,list):
			print2(item)
		else:
			print(item)

			
>>> print2(members)
zwx
yjl
wyz
cal
cf
male
20
180cm
60kg
>>> import sys; sys.path
['', 'D:\\Python33\\Lib\\idlelib', 'C:\\Windows\\SYSTEM32\\python33.zip', 'D:\\Python33\\DLLs', 'D:\\Python33\\lib', 'D:\\Python33', 'D:\\Python33\\lib\\site-packages']
>>> 
