import glob
import pickle

def lookup_stack_files():
	stack_files = glob.glob('*.stk')
	return stack_files

def get_valid_files(file):
	stack_files = lookup_stack_files()
	if file in stack_files:
		return file

def read_stack_files(stack_files):

	contents = [] 
	for stack_file in stack_files:
		file = open(stack_file, 'rb')
		processed = pickle.load(file)
		contents.append(processed)
		file.close()
		
	return contents 

