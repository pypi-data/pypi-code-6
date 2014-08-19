# -*- coding: utf-8 -*-
from operator import itemgetter
from functools import wraps
from time import time
from random import choice
from dill.source import getsource as source2
import os
import re
rows, columns = os.popen('stty size', 'r').read().split()

VERBOSE = True
unique_benchmark_variable_name = "ASDFASDFSHFDKBDKNBKDNFGBKNDKFGBNKDNFGBNJADSUHFAUHDJ" 

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

colors = [color.PURPLE,color.CYAN,color.DARKCYAN,color.GREEN,color.YELLOW,color.RED]
func_cache = {}
analyzed_cache = {}
percentage_cache = {}
parameters = {}

def bold(string):
	return "%s%s%s" % (color.BOLD, string,color.END)
def white(string):
	return "%s%s%s" % (color.DARKCYAN, string, color.END)

def bold_print(string):
	print color.BOLD	
	print color.RED	
	print string
	print color.END	

def purple_print(string):
	print color.PURPLE		
	print string
	print color.END	

def solid_line():
	print bold("-" * (int(columns) - 2))
	
def benchmark(groupname,name):
	try:
		func_cache[groupname].append([name,None])
	except KeyError:
		func_cache[groupname] = [[name,None]]
	def inner_benchmark(func):
		func_cache[groupname][-1][1] = func
		@wraps(func)
		def wrapper(*args,**kwargs):
			return func(*args, **kwargs)
		return wrapper
	return inner_benchmark

def analyze_metrics(stats):
	avgs = []
	for key in stats:
		avgs.append([stats[key]["name"], stats[key]["avg"],0])
	avgs.sort(key=lambda tup: tup[1])
	const = 1 / avgs[0][1]
	for item in avgs:
		item[2] = item[1] * const 
	return {"averages": avgs, "raw": stats}

def display(data):
	stats = data["averages"]
	raw = data["raw"]
	for item in stats:
		name = item[0]
		score = item[2]
		name = bold(white(name)) + " \n Total Time: %sms \n Average Repition: %sms" % (raw[name]["total"], raw[name]["avg"])
		text = " "
		for x in xrange(min(int(score),int(columns) - 1)): text += "█"
		print choice(colors), white(bold(name)) , "\n", text, color.END

def get_indents(old):
	indents = []
	for line in old:
		indent = ""
		for x in xrange(1,len(line)):
			temp = line[:x]
			if temp.isspace():
				indent = temp
			else:
				break
		indents.append(indent)
	return indents

def analyze_times(start,clockpoints):
	func = clockpoints[0]
	times = analyzed_cache.get(func,{})
	first = True
	for tup in clockpoints:
		if first:
			first = False
			continue
		time = tup[0]
		line_num = tup[1]
		elapsed = (time - start)
		if line_num in times:
			times[line_num] += elapsed
		else:
			times[line_num] = elapsed
		start += (time - start)
	analyzed_cache[func] = times
	
def scale_cache():
	for key in analyzed_cache:
		unscaled = analyzed_cache[key]
		minim = float("inf")
		for subkey in unscaled:
			minim = min(unscaled[subkey],minim) if unscaled[subkey] > 0 else minim
		coef = 1 / minim
		maxim = float("-inf")
		for subkey in unscaled:
			unscaled[subkey] = unscaled[subkey] * coef
			maxim = max(maxim,unscaled[subkey])
		coef2 = (int(columns) * .35) / maxim
		for subkey in unscaled:
			unscaled[subkey] = unscaled[subkey] * coef2	
	

def insert_clock_calls(old,indents,group):
	
	def get_formatted_group_params(group):
		params = parameters[group]
		args = params[0][0]
		kwargs = params[0][1]
		if type(args) != tuple:
			return "(%s,**%s)" % (args, kwargs)
		else:
			return "(*%s,**%s)" % (args, kwargs)
		

	def is_special_line(line):
		reserved = ("elif","else","raise","yield","finally")
		for word in reserved:
			check = word in line
			if check: return check
		return False

	def get_return_calc(line):
		end_of_return = line.index("return") + 6
		command = line[end_of_return:].strip()
		command = unique_benchmark_variable_name + " = %s" % command
		new_return = "return %s" % unique_benchmark_variable_name
		return command, new_return

	name = old[0][:old[0].index("(")].split(" ")[-1]
	fixed_old = old[1:]
	fixed_indents = indents[1:]
	shift = 0
	initial_lines = len(fixed_indents)
	has_returned = False

	for x in xrange(len(fixed_indents)):
		line = fixed_old[x + shift]
		next_contains_special = is_special_line(fixed_old[(x + shift + 1) % len(fixed_old)])
		line_contains_return = "return" in fixed_old[(x + shift)]
		line_contains_special_return = line_contains_return and re.match("[^\(]*(\(.*\))[^\)]*",line)
		if line_contains_return:
			fixed_old.insert(x + shift, fixed_indents[x % len(fixed_indents)] + "analyze_times(start,clockpoints)")
			has_returned = True
			shift += 1
		if line_contains_special_return:
			new_calc_command, new_return = get_return_calc(line)
			fixed_old.pop(x + shift)
			fixed_old.insert(x + shift, fixed_indents[x % len(fixed_indents)] + new_return)
			fixed_old.insert(x + shift - 1, fixed_indents[x % len(fixed_indents)] + new_calc_command)
			fixed_old.insert(x + shift, fixed_indents[x % len(fixed_indents)] + "clockpoints.append((time(),%i))" % x)
			shift += 2
		if not line.isspace() and len(line) and not next_contains_special and x < len(fixed_indents) - 1:			
			fixed_old.insert(x + shift + 1, fixed_indents[(x + 1) % len(fixed_indents)] + "clockpoints.append((time(),%i))" % x)
			shift += 1

	if not has_returned:
		fixed_old.append(fixed_indents[-1] + "analyze_times(start,clockpoints)")

	fixed_old.insert(0,fixed_indents[0] + "start = time()")
	fixed_old.insert(1,fixed_indents[0] + "clockpoints = [\"%s\"]" % name)
	fixed_old.append(name + get_formatted_group_params(group))
	return "\n".join([old[0]] + fixed_old)

def morph(old,group):
	indents = get_indents(old)
	new = insert_clock_calls(old,indents,group)
	return new
			
def get_char_type_counts(line):
	line = line.rstrip()
	total_not = 0
	total_tabs = 0
	for char in line:
		if char == "\t":
			total_tabs += 1
		else:
			total_not += 1
	return total_tabs, total_not

def get_longest_line(source):
	most_chars = 0
	most_tabs = 0
	for line in source:
		tabs, not_tabs = get_char_type_counts(line)
		most_chars = max(not_tabs,most_chars)
		most_tabs = max(tabs,most_tabs)
	return {"tabs" : most_tabs, "chars" : most_chars}

def get_scaled_space(line,most_info):
	tabs, not_tabs = get_char_type_counts(line)
	string = "            "
	string += " " * (most_info["chars"] - not_tabs)
	string += "\t" * (most_info["tabs"] - tabs + 1)
	return string
	
def detailed_display(funcs,reps,group):

	for func in funcs:
		raw_source = source2(func[1]).rstrip().split("\n")[1:]
		new = morph(raw_source,group)
		globs = globals()
		scope = { "time" : globs["time"], "analyze_times" : globs["analyze_times"] }
		for x in xrange(reps): exec(new,scope)
	scale_cache()
	for func in funcs:
		line_stats = analyzed_cache[func[1].__name__]
		func_source = source2(func[1]).rstrip().split('\n')[1:]
		longest_length_info = get_longest_line(func_source)
		for x in xrange(len(func_source)):
			code = func_source[x]
			time = line_stats.get(x - 1, "0.0")
			data = "%sms" % time if VERBOSE else ""
			print bold(code), get_scaled_space(code,longest_length_info), "█" * int(float(time)), data
		print "\n"
		
def group_test(funcs, reps, group):
	stats = {}
	params = parameters[group]
	for x in xrange(len(funcs)):
		for param in params:
			func = funcs[x][1]
			start = time()
			args = param[0]
			if type(args) != tuple:
				for y in xrange(reps): func( args, **param[1])
			else:
				for y in xrange(reps): func(*args, **param[1])
			end = time()
			total = end - start
			avg = total / reps
			title = funcs[x][0]
			stats[title] = { "total" : total, "avg": avg , "name": title }
	display(analyze_metrics(stats))
	bold_print("Detailed display")	
	detailed_display(funcs, reps, group)

def execute_tests(reps):
	for group in func_cache:
		functions = func_cache[group]
		solid_line()
		bold_print("GROUP: %s results after %i reps " % (group,reps))		
		group_test(functions,reps,group)
	solid_line()