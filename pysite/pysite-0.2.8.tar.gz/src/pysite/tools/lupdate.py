#!/usr/bin/python
# -*- coding: utf-8 -*-
from jinja2 import Environment
from jinja2.nodes import Getitem,Getattr,Const,Name,Call
import os,re,pprint
import imp,ast,sys
import xml.dom.minidom as minidom
from os.path import relpath,dirname
from pysite.compat import PORTABLE_STRING,portable_string
from slimit.parser import Parser
from slimit.visitors import nodevisitor
from slimit import ast as jsast

rx_rmquotes = re.compile(u'^["\'](.+)["\']$')

parser = Parser()


if sys.version_info[0]==2:
	arg_name_attr = 'id'
elif sys.version_info[0]>=3:
	arg_name_attr = 'arg'

global_transdict = {}
global_first_located = {}

def update_transdict(context,source,filename,lineno,comment=''):
	global global_transdict
	if context not in global_transdict:
		global_transdict[context] = {}
		global_first_located[context] = {}
	if source not in global_transdict[context]:
		global_transdict[context][source] = []
		global_first_located[context][source] = {}
	if comment not in global_transdict[context][source]:
		global_transdict[context][source] += [comment]
		global_first_located[context][source][comment] = [filename,PORTABLE_STRING(lineno)]

#Module
  #ClassDef
    #Name
      #Load
    #FunctionDef
      #arguments
        #Name
          #Param
      #Expr
        #Call
          #Attribute
            #Name
              #Load
            #Load
          #Str

def parse_subhandler(context):
	translate_args = ['source','context','comment','lang']
	fname = PORTABLE_STRING('subhandlers/%s.py' % context)
	sys.stdout.write(u"Parsing: %s... " % fname)
	transcnt = 0
	a = ast.parse(open(fname).read())
	encoding = 'utf-8'
	for obj in a.body:
		# init function version
		if isinstance(obj,ast.FunctionDef) and obj.name=='init':
			translator_id = getattr(obj.args.args[3],arg_name_attr)
			for n in ast.walk(obj):
				if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id==translator_id:
					acnt = 0
					args = {
						'source':None,
						'context':context if type(context)==PORTABLE_STRING else PORTABLE_STRING(context,encoding),
						'comment':PORTABLE_STRING('')}
					for arg in n.args:
						if isinstance(arg,ast.Str):
							args[translate_args[acnt]] = arg.s if type(arg.s)==PORTABLE_STRING else PORTABLE_STRING(arg.s,encoding)
						acnt+=1
					for kwarg in n.keywords:
						args[kwarg.arg] = kwarg.value.s if type(kwarg.value.s)==PORTABLE_STRING else PORTABLE_STRING(kwarg.value.s,encoding)
					update_transdict(args['context'],args['source'],fname,n.lineno,args['comment'])
					transcnt += 1
		if isinstance(obj,ast.ClassDef):
			for cw in ast.walk(obj):
				#for attr in dir(cw):
					#if not attr.startswith('_'):
						#print cw,attr,getattr(cw,attr)
				if isinstance(cw,ast.Call):
					for fw in ast.walk(cw):
						if isinstance(fw,ast.Attribute):
							if fw.attr=='translate':
								acnt = 0
								args = {
									'source':None,
									'context':context if type(context)==PORTABLE_STRING else PORTABLE_STRING(context,encoding),
									'comment':PORTABLE_STRING('')}
								for arg in cw.args:
									if isinstance(arg,ast.Str):
										args[translate_args[acnt]] = arg.s if type(arg.s)==PORTABLE_STRING else PORTABLE_STRING(arg.s,encoding)
									acnt+=1
								for kwarg in cw.keywords:
									args[kwarg.arg] = kwarg.value.s if type(kwarg.value.s)==PORTABLE_STRING else PORTABLE_STRING(kwarg.value.s,encoding)
								update_transdict(args['context'],args['source'],fname,cw.lineno,args['comment'])
								print(args['context'],args['source'],fname,cw.lineno,args['comment'])
								transcnt += 1
								#for a in ast.walk(cw):
									#if isinstance(a,
									#for attr in dir(a):
										#if not attr.startswith('_'):
											#print a,attr,getattr(a,attr)
							
				#if isinstance(cw,ast.FunctionDef):
					#for fw in ast.walk(obj):
						#if isinstance(fw,ast.Call):
							#attrib = getattr(getattr(fw.func,'value',None),'id',None)
							#if attrib=='self':
								#for aw in ast.walk(getattr(fw.func,'value',None)):
									#print aw
			
	print(u'Found %d translations' % transcnt)

def parse_jinja_template(context):
	translate_args = ['source','context','comment','lang']
	e = Environment()
	fname = PORTABLE_STRING('templates/%s.jinja' % context)
	sys.stdout.write(u"Parsing: %s... " % fname)
	stream = open(fname,'rb')
	encoding = 'utf-8'
	transcnt = 0
	t = e.parse(PORTABLE_STRING(stream.read(),encoding))
	for it in t.find_all(Getitem):
		if isinstance(it.node,Name) and it.node.name=='tr' and isinstance(it.arg,Const):
			update_transdict(context,it.arg.value,fname,it.node.lineno)
	for it in t.find_all(Getattr):
		if isinstance(it.node,Name) and it.node.name=='tr':
			update_transdict(context,it.attr,fname,it.node.lineno)
	for it in t.find_all(Getitem):
		if isinstance(it.node,Name) and it.node.name=='tr_common' and isinstance(it.arg,Const):
			update_transdict('common',it.arg.value,fname,it.node.lineno)
	for it in t.find_all(Getattr):
		if isinstance(it.node,Name) and it.node.name=='tr_common':
			update_transdict('common',it.attr,fname,it.node.lineno)
	for it in t.find_all(Call):
		if isinstance(it.node,Name) and it.node.name=='translate':
			acnt = 0
			args = {
				'source':None,
				'context':portable_string(context,encoding),
				'comment':PORTABLE_STRING('')}
			for arg in it.args:
				if isinstance(arg,Const):
					args[translate_args[acnt]] = portable_string(arg.value,encoding)
				acnt+=1
			for kwarg in it.kwargs:
				args[kwarg.key] = portable_string(kwarg.value.value,encoding)
			update_transdict(args['context'],args['source'],fname,it.node.lineno,args['comment'])
			transcnt += 1
	print(u'Found %d translations' % transcnt)

def parse_js(jsfpath):
	sys.stdout.write(u"Parsing: %s... " % jsfpath)
	def parse_string_arg(node):
		if isinstance(node,jsast.String):
			m = rx_rmquotes.match(node.value)
			if m:
				return m.groups()[0]
			return u''
		if isinstance(node,jsast.BinOp):
			left = parse_string_arg(node.left)
			right = parse_string_arg(node.right)
			return left+right

	def_context = u'js_%s' % os.path.splitext(os.path.basename(jsfpath))[0]
	f = open(jsfpath,'rb')
	jsdata = PORTABLE_STRING(f.read(),'utf-8')
	f.close()
	
	transcnt = 0
	tree = parser.parse(jsdata)
	for node in nodevisitor.visit(tree):
		pnames = ['source','context','comment']
		if isinstance(node,jsast.FunctionCall):
			ival = getattr(node.identifier,'value','')
			if ival in [u'pysite_tr',u'pysite_tr_common',u'pysite_translate']:
				args = []
				for arg in node.children()[1:]:
					args += [parse_string_arg(arg)]
				if len(args)==0:
					print("No arguments - skipping")
				comment = u''
				context = def_context
				if node.identifier.value=='pysite_tr':
					source = args[0]
					if len(args)>1:
						comment = args[1]
				elif node.identifier.value=='pysite_tr_common':
					context = u'js_common'
					source = args[0]
					if len(args)>1:
						comment = args[1]
				elif node.identifier.value=='pysite_translate':
					source = args[0]
					if len(args)==3:
						context = args[1]
						comment = args[2]
					elif len(args)==2:
						context = args[1]
					if context.find(u'js_')!=0:
						context = u'js_%s' % context
				update_transdict(context,source,jsfpath,1,comment)
				transcnt += 1
	print(u'Found %d translations' % transcnt)

def parse_ts(ts_fname):
	doc = minidom.parse(open(ts_fname))
	tr_dict = {}
	for ctx_elem in doc.getElementsByTagName('context'):
		name = ctx_elem.getElementsByTagName('name')[0]
		context = name.childNodes[0].data
		tr_dict[context] = {}
		for msg_elem in ctx_elem.getElementsByTagName('message'):
			src_elem = msg_elem.getElementsByTagName('source')
			if not len(src_elem):
				continue
			source = src_elem[0].childNodes[0].data
			if source not in tr_dict[context]:
				tr_dict[context][source] = {}

			comment = PORTABLE_STRING('')
			c_elem = msg_elem.getElementsByTagName('comment')
			if len(c_elem):
				comment = c_elem[0].childNodes[0].data
			if comment not in tr_dict[context][source]:
				tr_dict[context][source][comment] = {}
			
			translation = None
			tr_elem = msg_elem.getElementsByTagName('translation')
			if len(tr_elem):
				if len(tr_elem[0].childNodes):
					translation = tr_elem[0].childNodes[0].data
				tr_dict[context][source][comment]['type'] = None
				if tr_elem[0].hasAttribute('type'):
					tr_dict[context][source][comment]['type'] = tr_elem[0].getAttribute('type')
			tr_dict[context][source][comment]['translation'] = translation
			
			filename = None
			line = None
			l_elem = msg_elem.getElementsByTagName('location')
			if len(l_elem):
				filename = l_elem[0].getAttribute('filename')
				line = l_elem[0].getAttribute('line')
			tr_dict[context][source][comment]['filename'] = filename
			tr_dict[context][source][comment]['line'] = line
	return tr_dict

def rebuild_ts(ts_dict,language,filename_pathprefix):
	global global_transdict,global_first_located
	doc = minidom.Document()
	ts = doc.createElement('TS')
	ts.setAttribute('version','2.0')
	ts.setAttribute('language',language)
	doc.appendChild(ts)
	for context,sources in global_transdict.items():
		context_elem = doc.createElement('context')
		name = doc.createElement('name')
		name.appendChild(doc.createTextNode(context))
		context_elem.appendChild(name)
		ts.appendChild(context_elem)
		for k,v in sources.items():
			for comment in v:
				msg_elem = doc.createElement('message')
				loc_elem = doc.createElement('location')
				filename = os.path.join(filename_pathprefix,global_first_located[context][k][comment][0])
				loc_elem.setAttribute('filename',filename)
				loc_elem.setAttribute('line',global_first_located[context][k][comment][1])
				msg_elem.appendChild(loc_elem)
				src_elem = doc.createElement('source')
				src_elem.appendChild(doc.createTextNode(k))
				msg_elem.appendChild(src_elem)
				if comment:
					commen_elem = doc.createElement('comment')
					commen_elem.appendChild(doc.createTextNode(comment))
					msg_elem.appendChild(commen_elem)
				tr_elem = doc.createElement('translation')
				try:
					tr = ts_dict[context][k][comment]['translation']
					tr_elem.appendChild(doc.createTextNode(tr))
					if ts_dict[context][k][comment]['type']:
						tr_elem.setAttribute('type',ts_dict[context][k][comment]['type'])
				except:
					tr_elem.setAttribute('type','unfinished')
				msg_elem.appendChild(tr_elem)
				context_elem.appendChild(msg_elem)
	for context,sources in ts_dict.items():
		ctx_elem = None
		for it_ctx in doc.getElementsByTagName('context'):
			name_elem = it_ctx.getElementsByTagName('name')
			if name_elem[0].childNodes[0].data == context:
				ctx_elem = it_ctx
				break
		if not ctx_elem:
			ctx_elem = doc.createElement('context')
			name = doc.createElement('name')
			name.appendChild(doc.createTextNode(context))
			ctx_elem.appendChild(name)
			ts.appendChild(ctx_elem)

		for source,comments in sources.items():
			for comment,trinfo in comments.items():
				if trinfo['translation']:
					if context not in global_transdict or source not in global_transdict[context] or not global_transdict[context][source].count(comment):
						msg_elem = doc.createElement('message')
						src_elem = doc.createElement('source')
						src_elem.appendChild(doc.createTextNode(source))
						msg_elem.appendChild(src_elem)
						if comment:
							commen_elem = doc.createElement('comment')
							commen_elem.appendChild(doc.createTextNode(comment))
							msg_elem.appendChild(commen_elem)
						tr_elem = doc.createElement('translation')
						tr_elem.appendChild(doc.createTextNode(trinfo['translation']))
						tr_elem.setAttribute('type','obsolete')
						msg_elem.appendChild(tr_elem)
						ctx_elem.appendChild(msg_elem)
	return doc.toxml(encoding='utf-8')

parsed_already = False

def parse_all():
	global parsed_already
	if parsed_already:
		return
	parsed_already = True
	flist = os.listdir('templates')
	for fname in flist:
		m = re.match('^([^\.]+)\.jinja$',fname)
		if m:
			parse_jinja_template(m.groups()[0])

	flist = os.listdir('subhandlers')
	for fname in flist:
		m = re.match('^([^\.]+)\.py$',fname)
		if m:
			parse_subhandler(m.groups()[0])

	for bdir,dirs,files in os.walk('static'):
		for fname in files:
			if fname.endswith('.js') and not fname=='pysite.js':
				parse_js(os.path.join(bdir,fname))

def lupdate(ts_fname,language):
	parse_all()
	ts_dict = {}
	filename_pathprefix = relpath('.',dirname(ts_fname))
	if not os.path.exists(dirname(ts_fname)):
		os.makedirs(dirname(ts_fname))
		f = open("%s/__init__.py" % dirname(ts_fname),'w')
		f.close()
	if os.path.exists(ts_fname):
		ts_dict = parse_ts(ts_fname)
	res=rebuild_ts(ts_dict,language,filename_pathprefix)
	open(ts_fname,'wb').write(res)

if __name__=='__main__':
	if len(sys.argv)<3:
		sys.stderr.write("usage: %s <ts-file> <lang-code>\n" % sys.argv[0])
		sys.stderr.write("Example: %s admin_da.ts da_DK\n" % sys.argv[0])
		sys.exit(1)

	lupdate(sys.argv[1],sys.argv[2])
