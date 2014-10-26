# coding: utf-8
"""
File ID: 6jpE0pD
"""

from argparse import ArgumentParser
import os.path
import sys
try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

def make_new_file_path(path):
    """
    Given a file path, if there is existing file on the path,
    transform the path by adding incremented number postfix,
    until there is no existing file on the path.
    """
    #/
    path_noext, ext = os.path.splitext(path)
    
    #/
    new_path = path
    
    #/
    cnt = 1
    while os.path.exists(new_path):
        cnt += 1

        new_path = '{}_{}{}'.format(path_noext, cnt, ext)
        
    #/
    return new_path

def create_url_file(url, output_dir=None):
    #/ 8kvs7Ez
    #/ handle no scheme case
    ## E.g. call |urlsplit| with |'pypi.python.org/'| returns
    ##  SplitResult(scheme='', netloc='', path='pypi.python.org/', query='', fragment='')
    ##  due to the missing scheme |http://|.
    part_s = urlparse.urlsplit(url)
    
    scheme = part_s[0]

    if not scheme:
        url = 'http://' + url
    
        part_s = urlparse.urlsplit(url)
        
        assert part_s[0]

    #/
    netloc = part_s[1]
    
    path = part_s[2]
    
    #/ 7fOTIhs
    #/ replace |/| with |--|
    ## E.g.
    ##  pypi.python.org/pypi
    ##  becomes
    ##  pypi.python.org--pypi
    url_file_name = netloc + path.replace('/', '--')
    
    #/ 5cmN4hs
    #/ escape other special characters
    url_file_name = quote(url_file_name)
    
    #/ 5rFuPj4
    #/ add query part
    query = part_s.query

    if query:
        url_file_name = '{}@{}'.format(url_file_name, query)
        ## assume query content is escaped already
        ##
        ## use |@| to replace |?|
    
    #/ 2aFlar8
    #/ add fragment part
    fragment = part_s.fragment

    if fragment:
        url_file_name = '{}#{}'.format(url_file_name, fragment)
        ## assume fragment content is escaped already
    
    #/ 7qAEmu6
    #/ strip ending |-|
    url_file_name = url_file_name.rstrip('-')
    
    #/ 9iOAWsx
    #/ add extension
    url_file_name = url_file_name + '.url'
    
    #/ 3sLG8wi
    #/ make file path
    if output_dir:
        url_file_path = os.path.join(output_dir, url_file_name)
    else:
        url_file_path = url_file_name
    
    #/ 7tXovWb
    #/ ensure file path is not existing
    url_file_path = make_new_file_path(url_file_path)
    
    #/ 5p1DFhl
    #/ make file content
    url_file_content = '[InternetShortcut]\nURL={}'.format(url)
    
    #/ 7xWXnF7
    #/ write to file
    f = open(url_file_path, mode='w')
    f.write(url_file_content)
    f.close()
    
    #/
    return (url, url_file_path)

#/
PROG_NAME = 'aoikutf'
ARG_K_URL_K_DEST = 'url'
ARG_K_OUTPUT_DIR = '-d'
ARG_K_OUTPUT_DIR_K_DEST = 'output_dir'
ARG_K_SCHEME = '-s'
ARG_K_SCHEME_K_DEST = 'scheme'
ARG_K_SCHEME_V_DFR = 'aoikutf'
ARG_K_REG = '--reg'
ARG_K_REGARG_K_DEST = 'reg'

ARG_HELP_TT_D = {
    ARG_K_URL_K_DEST: r'URL used to create the url file.',
    ARG_K_OUTPUT_DIR_K_DEST: r'Output dir.',
    ARG_K_SCHEME_K_DEST: r"AoikUrlToFile's URL scheme. By default |{}|.".format(ARG_K_SCHEME_V_DFR),
    ARG_K_REGARG_K_DEST: r'Generate |.reg| file data and write to stdout.',
}

TT_D = {
    'F7Th4jo': """Error: Output dir for the command in the |.reg| file content is not specified.
Please use cmd arg |{}| to specify one.""".format(ARG_K_OUTPUT_DIR),
    'HdMpmE4': 'Error: URL is not specified.',
}

def make_arg_parser(tt):
    #/ 5nLmzFh
    parser = ArgumentParser(prog=PROG_NAME, add_help=True)
    
    parser.add_argument(
        ARG_K_URL_K_DEST,
        nargs='?', ## 2rYrLdD
        metavar='URL',
        help=tt(ARG_K_URL_K_DEST),
    )
    
    parser.add_argument(
        ARG_K_OUTPUT_DIR,
        dest=ARG_K_OUTPUT_DIR_K_DEST,
        metavar='OUTPUT_DIR',
        help=tt(ARG_K_OUTPUT_DIR_K_DEST),
    )
    
    parser.add_argument(
        ARG_K_SCHEME,
        dest=ARG_K_SCHEME_K_DEST,
        metavar='SCHEME',
        help=tt(ARG_K_SCHEME_K_DEST),
    )
    
    parser.add_argument(
        ARG_K_REG,
        dest=ARG_K_REGARG_K_DEST,
        action='store_true',
        help=tt(ARG_K_REGARG_K_DEST),
    )
    
    return parser

RET_V_OK = 0
RET_V_REG_GENERATED_OK = 0
RET_V_REG_CMD_OUTPUT_DIR_NOT_SPECIFIED_ERR = 1
RET_V_URL_NOT_SPECIFIED_ERR = 2

def main():
    #/
    def parser_tt(key):
        return ARG_HELP_TT_D[key]
    
    #/ 4efdt3N
    parser = make_arg_parser(tt=parser_tt)
    
    #/ 7s74u0j
    args_obj = parser.parse_args()
    #/ 6vfzJ4f
    ## exit inside |parse_args| if has error
    
    #/
    def tt(key):
        return TT_D[key]
    
    #/
    scheme = getattr(args_obj, ARG_K_SCHEME_K_DEST) or ARG_K_SCHEME_V_DFR
    
    #/
    output_dir = getattr(args_obj, ARG_K_OUTPUT_DIR_K_DEST)
    
    #/
    output_reg = getattr(args_obj, ARG_K_REGARG_K_DEST)
    
    #/ 9mqTx9o
    if output_reg:
        #/ 2swbnQM
        if not output_dir:
            #/ 6b3vLj1
            msg = tt('F7Th4jo')
            
            sys.stderr.write(msg)
            
            #/ 4pjTZhc
            return RET_V_REG_CMD_OUTPUT_DIR_NOT_SPECIFIED_ERR
        
        #/ 3ePU4Q6
        reg_fmt = r'''REGEDIT4
[HKEY_CLASSES_ROOT\{scheme}\shell\open\command]
@="\"{py_exe}\" \"{py_file}\" -d \"{output_dir}\" \"%1\""'''
        
        reg_data = reg_fmt.format(
            scheme=scheme.replace('\\', r'\\').replace(r'"', r'\"'),
            py_exe=sys.executable.replace('\\', r'\\').replace(r'"', r'\"'),
            py_file=__file__.replace('\\', r'\\').replace(r'"', r'\"'),
            output_dir=output_dir.replace('\\', r'\\').replace(r'"', r'\"'),
        )
        
        #/ 7m9SS39
        sys.stdout.write(reg_data)
        
        #/ 3yRaqT4
        return RET_V_REG_GENERATED_OK
    
    #/
    url = getattr(args_obj, ARG_K_URL_K_DEST)
    ## can be None due to |nargs| at 2rYrLdD
    
    #/ 2swbnQM
    if not url:
        #/ 9mYbhY1
        msg = tt('HdMpmE4')
        
        sys.stdout.write(msg)
        
        #/ 2dkvAhx
        return RET_V_URL_NOT_SPECIFIED_ERR
    
    #/ 7oiKPc7
    #/ remove scheme prefix in the url
    ## E.g.
    ##  aoikutf://pypi.python.org
    ##  aoikutf://https://pypi.python.org
    scheme_prefix = scheme + r'://'
    
    if url.startswith(scheme_prefix):
        url = url[len(scheme_prefix):]
    
    #/ 7cxv5GB
    url, url_file_path = create_url_file(
        url=url,
        output_dir=output_dir,
    )

    #/ 8f2FJUA
    print('{}\nto\n{}'.format(url, url_file_path))
    
    #/ 4aAEFUP
    return RET_V_OK
    
if __name__ == '__main__':
    sys.exit(main())
