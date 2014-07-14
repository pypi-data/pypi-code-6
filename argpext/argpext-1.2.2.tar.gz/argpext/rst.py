#!/usr/bin/env python

import shlex
import stat
import shutil
import os
import io
import sys
import subprocess
import code
import xml, xml.dom.minidom

import argpext
from argpext.prints import *

CONTENT = argpext.KeyWords(['python','shell'])
ACTIONS = argpext.KeyWords(['show','execute'])
XMLKEYS = argpext.KeyWords(['input'])

class Debug(object):
    KEYS = argpext.KeyWords(['p','x','k'])
    def __init__(self,key=None):
        K = set([Debug.KEYS(k) for k in key]) if key is not None else set()
        self.show_position = 'p' in K
        self.exit_on_error = 'x' in K
        self.disable_save_as = 'k' in K


class __NoDefault: pass

def get_nodeattr(node,key,default=__NoDefault()):
    if isinstance(default,__NoDefault):
        q = node.attributes.get(key)
        if q is None: raise ValueError('mandatory key value missing for %s' % key)
        return getattr(q,'value')
    else:
        return getattr(node.attributes.get(key),'value', default)


class Reconnect(object):
    def __init__(self,stdout,stderr):
        self._so = sys.stdout
        self._se = sys.stderr
        sys.stdout = stdout
        sys.stderr = stderr

    def __enter__(self): pass

    def __exit__(self,exc_type, exc_value, traceback):
        sys.stdout = self._so
        sys.stderr = self._se
        return True # Suppresses the exception


def filter_out_tr(q):
    "Filter out the traceback messages"
    L = []
    if len(q):
        q = q.splitlines()
        for q in q:
            if q.startswith('Traceback '): continue
            if q.startswith(' '): continue
            L += [q]
    q = os.linesep.join(L)
    return q



def process_shell(text):

    output_all = []
    for command in text.splitlines():

        def prn(line,file):
            file.write(line)
            file.write(os.linesep)

        # When passing with shell=True, you do not need to split the command into list.
        proc = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True )
        proc.wait()
        ierr = proc.returncode

        L = []

        # Deal with stdout
        so = ''
        q = proc.stdout.read().decode()
        if len(q):
            q = q.splitlines()
            for q in q:
                q = q.replace('usage: ./','usage: ')
                so += (q+os.linesep)

        # Deal with stderr
        se = ''
        q = proc.stderr.read().decode()
        q = filter_out_tr(q)
        for line in q.splitlines():
            se += (line+os.linesep)


        prm = '$ '+command+os.linesep

        output = prm+so+se
        output_all += [output]


    return dict(ierr=ierr,output='\n'.join(output_all))



def process_python(text):

    R = []
    def pnl(q):
        if len(q): q += os.linesep
        return q

    cons = code.InteractiveConsole()

    start = [
        "__name__ = '__main__'"
        ,"import sys"
        ,"sys.argv = ['excode.py']"
        ,'del sys'
        ]
    for q in start:
        cons.push(q)


    for line in text.splitlines():

        line = line.rstrip()

        stdout = io.StringIO()
        stderr = io.StringIO()

        with Reconnect(stdout=stdout,stderr=stderr):
            status = cons.push(line)
        stdout.seek(0)
        stderr.seek(0)


        prompt = '... ' if status else '>>> '

        prm = '%s%s' % ( prompt, line )+os.linesep
        so = pnl(str(stdout.read()))
        se = pnl(filter_out_tr(str(stderr.read())))
        output = prm+so+se
        #print('[%s]' % output)
        R += [output]

    return dict(ierr=0,output=''.join(R))


def parse_node(node,debug):
    content = CONTENT(get_nodeattr(node,'content'))
    action = ACTIONS(get_nodeattr(node,'action'))

    text = node.childNodes[0].data.strip()

    def manage_save_as():
        save_as = get_nodeattr(node,'save_as',None)
        if save_as is not None:
            if debug.disable_save_as: return
            pri('writing file:', save_as)
            with open(save_as,'w') as fho:
                if content == 'python':
                    fho.write('#!/usr/bin/env python\n\n')
                fho.write( text )
            os.chmod(save_as,stat.S_IXUSR|stat.S_IRUSR|stat.S_IWUSR)

    manage_save_as()


    if action == "show":
        pass
    elif action == "execute":
        q = {'shell' :  process_shell, 
             'python' : process_python,
             }[content](text)
        text = q['output']
        ierr = q['ierr']

        if ierr and debug.exit_on_error:
            pri(text,exit=0)


    return text



def xmlgen(inputfile,outputfile,debug):

    def process(iline,text,block_ident):
        print('processing....')
        try:
            dom = xml.dom.minidom.parseString(text)
        except:
            print( text, file=sys.stderr )
            raise ValueError('XML not well-formed, see above')

        node = dom.childNodes[0]

        text = parse_node(node,debug)

        def f(text):
            T = []
            full_ident = block_ident+' '*2
            T += [block_ident+'::']
            T += [block_ident]
            for line in text.splitlines():
                T += [full_ident+line]
            if debug.show_position:
                T += [full_ident]
                T += [full_ident+'# File %s, line %d' % (os.path.basename(inputfile), iline)]
            T += [block_ident+'..']
            T += [block_ident]
            T = '\n'.join(T)
            return T

        text = f(text)
        #pri(text,exit=2)
        return text



    def simple_parse():
        chunk = []


        with open(outputfile,'w') as fho:

            write = (lambda x: print(x,file=fho))

            for iline,line in enumerate(open(inputfile),1):
                line = line.rstrip('\r\n')
                dump = None
                textline = None

                if len(chunk) == 0:
                    q = line.find('<%s' % XMLKEYS('input'))
                    if q != -1:
                        block_ident = ' '*q
                        pri(q)
                        pri('BI[%s]' % block_ident)
                        chunk += [line]
                    else:
                        textline = line
                else:
                    chunk += [line]
                    if line.startswith('</%s>' % XMLKEYS('input') ):
                        dump = '\n'.join(chunk)
                        chunk = []

                print('[%d %s]' % ( iline, line) )

                if dump is not None:
                    #pri(dump,exit=4)
                    #pri('[%s]' % block_ident)
                    q = process(iline,dump,block_ident)
                    write( q )
                    del block_ident

                if textline is not None:
                    write(line)



    PATH_INI = os.environ['PATH']
    PYTHONPATH_INI = os.environ.get('PYTHONPATH')
    SYS_PATH_INI = sys.argv

    with argpext.ChDir('doc.tmp') as workdir:

        extra_paths = [workdir.initdir,os.getcwd()]

        os.environ['PYTHONPATH'] = os.path.pathsep.join(extra_paths+([] if PYTHONPATH_INI is None else [PYTHONPATH_INI]))
        os.environ['PATH'] = os.path.pathsep.join(extra_paths+[PATH_INI])
        sys.path = extra_paths+sys.path
        

        inputfile=os.path.join(workdir.initdir,inputfile)
        outputfile=os.path.join(workdir.initdir,outputfile)
        simple_parse()

    # Restore paths
    os.environ['PATH'] = PATH_INI

    if PYTHONPATH_INI is not None:
        os.environ['PYTHONPATH'] = PYTHONPATH_INI
    else:
        del os.environ['PYTHONPATH']

    




class Main(argpext.Task):

    hook = argpext.make_hook(xmlgen)

    def populate(self,parser):
        parser.add_argument('-d',dest='debug',type=Debug,default=Debug(),help="Debug mode")
        parser.add_argument('-i',dest='inputfile',default='doc.rst',
                            help='Input .rst file. The default is "%(default)s"')
        parser.add_argument('-o',dest='outputfile',default='index.rst', 
                            help='Output file. The default value is "%(default)s".')





