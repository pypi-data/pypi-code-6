# coding: utf-8
"""
File ID: 5w5IzOY
"""

from aoiksixyio import SixyIO
from aoiki18n import I18n
import os.path
import re
import sys
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse
        
try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote
    
#/
def make_file_name_by_url(url):
    #/
    part_s = urlparse.urlsplit(url)

    #/
    host = part_s[1]

    if not host:
        url = u'http://' + url
    
        part_s = urlparse.urlsplit(url)

    #/
    host = part_s[1]
    
    path = part_s[2]
    
    file_name = quote(host + path.replace(u'/', u'--'))
    
    #/
    query = part_s.query

    if query:
        file_name = u'{}@{}'.format(file_name, query)

    #/
    fragment = part_s.fragment

    if fragment:
        file_name = u'{}#{}'.format(file_name, fragment)
    
    #/
    file_name = file_name.strip(u'-')
    
    #/
    return file_name
    
#/
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

        new_path = u'{}_{}{}'.format(path_noext, cnt, ext)
        
    #/
    return new_path

#/
ARG_K_SHOW_ENCODING_INFO = '--ei'
ARG_K_SHOW_LOCALE_INFO = '--li'
ARG_K_SHOW_LOCALE_CHOICES = '--lc'
ARG_K_DEBUG_ON = '--debug'
ARG_K_HELP_ON = '-h'

def make_arg_parser(cls, tt=None):
    #/
    tt = tt or (lambda x: x)
    
    #/ 5nLmzFh
    parser = cls(prog=tt('aoikbtf'), add_help=False)
    
    mutex_grp = parser.add_mutually_exclusive_group()
    
    parser.add_argument(
        'input_file_path',
        metavar='INPUT_FILE',
        help=tt('FFE4OvD'),
    )
    
    parser.add_argument(
        '-d',
        dest='output_dir_path',
        metavar='OUTPUT_DIR',
        help=tt('A3HgyZX'),
    )

    parser.add_argument(
        '--fmt-de',
        dest='fmt_is_de',
        action='store_true',
        help=tt('JDNfA1u'),
    )

    parser.add_argument(
        '--nbt',
        dest='name_by_title',
        action='store_true',
        help=tt('GZjKXz5'),
    )

    mutex_grp.add_argument(
        '--ete',
        dest='esc_to_empty',
        action='store_true',
        help=tt('B4SNjC2'),
    )

    mutex_grp.add_argument(
        '--ets',
        dest='esc_to_space',
        action='store_true',
        help=tt('GbzgvM3'),
    )
    
    parser.add_argument(
        '--stdioe',
        dest='stdioe',
        default=None,
        help=tt('CbGuoYc'),
    )
    
    parser.add_argument(
        '--stdie',
        dest='stdie',
        default=None,
        help=tt('G2HJHZo'),
    )
    
    parser.add_argument(
        '--stdoe',
        dest='stdoe',
        default=None,
        help=tt('CxIyunJ'),
    )
    
    parser.add_argument(
        '--stdee',
        dest='stdee',
        default=None,
        help=tt('I1V3xDr'),
    )
    
    parser.add_argument(
        '--cae',
        dest='cae',
        default=None,
        help=tt('ARaXz4H'),
    )
    
    #/ 9cCQk7p
    parser.add_argument(
        '--ife',
        dest='ife',
        default=None,
        help=tt('IVP1kgm'),
    )
    
    parser.add_argument(
        '--ofe',
        dest='ofe',
        default=None,
        help=tt('BB7ImCU'),
    )
    
    parser.add_argument(
        '--spie',
        dest='spie',
        default=None,
        help=tt('IPMSTyY'),
    )
    
    parser.add_argument(
        '--spoe',
        dest='spoe',
        default=None,
        help=tt('Dg53o1G'),
    )
    
    parser.add_argument(
        ARG_K_SHOW_ENCODING_INFO,
        dest='show_encoding_info',
        action='store_true',
        help=tt('FP3N30w'),
    )

    parser.add_argument(
        '-l',
        dest='ll_arg',
        metavar='LOCALE',
        help=tt('DucP7ae'),
    )
    
    parser.add_argument(
        ARG_K_SHOW_LOCALE_CHOICES,
        dest='show_locale_choices',
        action='store_true',
        help=tt('HGqtlE6'),
    )
    
    parser.add_argument(
        ARG_K_SHOW_LOCALE_INFO,
        dest='show_locale_info',
        action='store_true',
        help=tt('IMqVz8s'),
    )
    
    parser.add_argument(
        ARG_K_DEBUG_ON,
        dest='debug_on',
        action='store_true',
        help=tt('G9oKbur'),
    )
    
    parser.add_argument(
       ARG_K_HELP_ON,
       dest='help_on',
       action='store_true',
       help=tt('F79tqsA'),
    )
    
    return parser

MAIN_RET_V_OK = 0
MAIN_RET_V_SHOW_HELP = 0
MAIN_RET_V_SHOW_ENCODING_INFO = 0
MAIN_RET_V_SHOW_LOCALE_INFO = 0
MAIN_RET_V_SHOW_LOCALE_CHOICES = 0
MAIN_RET_V_INIT_I18N_ERR = 1
MAIN_RET_V_PYTHON_VER_NOT_SUPPORTED = 2
MAIN_RET_V_INIT_EASYIO_ERR = 3
MAIN_RET_V_DECODE_OUTPUT_DIR_PATH_ERR = 4
MAIN_RET_V_DECODE_INPUT_FILE_PATH_ERR = 5
MAIN_RET_V_OUTPUT_DIR_NOT_EXISTING = 6
MAIN_RET_V_OPEN_INPUT_FILE_ERR = 7
MAIN_RET_V_DECODE_INPUT_FILE_LINE_ERR = 8

def main():
    #/ 5kunyjN
    SixyIO.reload_default_encoding('utf-8')
    
    #/
    SixyIO.register_special_codecs()
    
    #/ 6r3nhoQ
    if (sys.version_info[0] == 2 and sys.version_info < (2, 7))\
    or (sys.version_info[0] > 2 and sys.version_info < (3, 2)):
        #/ 6iBzArq
        msg = u"""Error: Unsupported Python version.
Make sure your Python 2 version is >=2.7 or Python 3 version is >=3.2
"""
        
        SixyIO._stderr_write_safe(msg, encoding=SixyIO.STDIE_DFT)
        
        #/ 5neqPNn
        return MAIN_RET_V_PYTHON_VER_NOT_SUPPORTED
    
    #/
    from argparse import ArgumentParser
    
    #/ 9tgfTtQ
    tmp_parser = make_arg_parser(cls=ArgumentParser)
        
    #/
    tmp_args = list(sys.argv[1:])
    
    to_insert_parg = False
    
    if len(tmp_args) == 0:
        to_insert_parg = True
    else:
        option_s_need_no_parg = [
            ARG_K_SHOW_ENCODING_INFO,
            ARG_K_SHOW_LOCALE_INFO,
            ARG_K_SHOW_LOCALE_CHOICES,
            ARG_K_DEBUG_ON,
            ARG_K_HELP_ON,
        ]
        
        for option in option_s_need_no_parg:
            if option in tmp_args:
                to_insert_parg = True
                break
    
    #/
    if to_insert_parg:
        #/
        ## force add a positional argument,
        ##  to prevent |parse_known_args| below aborts.
        tmp_args.insert(0, '')
    
    #/ 5pWYIKp
    tmp_args_obj = tmp_parser.parse_known_args(args=tmp_args)[0]
    
    #/
    debug_on = tmp_args_obj.debug_on
    
    SixyIO.DEBUG_ON = debug_on
    
    #/
    ll_arg = tmp_args_obj.ll_arg
    ## None if not given
    
    ll_fb = 'en'
    
    #/
    I18n.yaml_force_unicode()
    
    i18n_dir = os.path.join(os.path.dirname(__file__), 'i18n')
    
    def path_func(ll):
        path = os.path.join(
            SixyIO.fse_to_u_safe(i18n_dir),
            SixyIO.lce_to_u_safe(ll) + I18n.TT_FILE_EXT_UTXT
        )
        return path
    
    i18n = None
    
    exc = None
    
    ll_s = I18n.get_locale_hints(cmdarg=ll_arg, fb=ll_fb)
    
    for ll in ll_s:
        try:
            i18n = I18n(locale=ll, locale_fallback=ll_fb, path_func=path_func)
            break
        except Exception as e:
            #/
            exc = e
            
            #/
            if ll_arg:
            ## This means user has specified a locale using cmd arg.
            ## In this case, stop without trying inferred ones.
                assert ll_arg == ll_s[0]
                break
            else:
            ## This means user has not specified a locale using cmd arg.
            ## In this case, keep trying inferred ones.
                continue
    
    #/
    if i18n is None:
        #/ 5yWBx8h
        assert exc
        
        err_typ = exc.args[0]
        
        if err_typ == I18n.LOAD_LOCALE_TT_FILE_ERR:
            path = SixyIO.lce_to_u_safe(path_func(ll))
        elif err_typ == I18n.LOAD_LOCALE_FALLBACK_TT_FILE_ERR:
            path = SixyIO.lce_to_u_safe(path_func(ll_fb))
        else:
            assert False
        
        #/ I18n can not be initialized. So only provide English msg.
        msg_fmt = u'Error: Failed loading i18n file for locale |{}|.\nPath is |{}|.\n'\
            .format(SixyIO.lce_to_u_safe(ll), path)
            
        msg = msg_fmt.format(path)

        SixyIO._stderr_write_safe(msg)
        
        #/
        if debug_on:
            SixyIO._stderr_write_tb_safe()
              
        #/ 4mCE3Al
        return MAIN_RET_V_INIT_I18N_ERR
    
    #/ 2dZ7vSY
    tt = i18n.tt
    
    #/ 7zrJzPc
    sio = SixyIO(
        stdioe=tmp_args_obj.stdioe,
        stdie=tmp_args_obj.stdie,
        stdoe=tmp_args_obj.stdoe,
        stdee=tmp_args_obj.stdee,
        cae=tmp_args_obj.cae,
        ife=tmp_args_obj.ife,
        ofe=tmp_args_obj.ofe,
        spie=tmp_args_obj.spie,
        spoe=tmp_args_obj.spoe,
        exit_code=MAIN_RET_V_INIT_EASYIO_ERR,
        tt=tt,
        debug_on=debug_on,
    )
    #/ 5oMILyz
    ## exit inside |init| if has error.
    
    #/
    def parser_tt(key, tt=tt):
        #/
        utxt = tt(key)
        
        #/
        if not SixyIO.IS_PY2:
            stxt = utxt
        else:
            stxt = utxt.encode(sio.stdee) if utxt is not None else None
        
        #/
        return stxt
    
    #/
    args = sys.argv[1:]
    
    #/ 4ykdL9b
    parser = make_arg_parser(cls=ArgumentParser, tt=parser_tt)
    
    #/ 8qf0bnK
    ## Because of |add_help=False| at 5nLmzFh, |-h| is no longer a special option.
    ## |parse_args| will print usage message if positional arguments are not enough,
    ##  even if |-h| is specified.
    ## We do not want this behavior. So handle it before calling |parse_args| at 2pePlsG.
    if tmp_args_obj.help_on:
        #/
        parser.print_help()
        
        #/
        return MAIN_RET_V_SHOW_HELP
    
    #/
    exit_code = None
    
    #/ 9aj6UHg
    if tmp_args_obj.show_encoding_info:
        #/
        sio.stderr_print_safe(tt('GnaSkZA'))
        sio.stderr_print_safe(sio.get_native_encodings_info())
        sio.stderr_print_safe(u'')
        
        #/
        sio.stderr_print_safe(tt('GSoLF46'))
        sio.stderr_print_safe(sio.get_sixyio_encodings_info())
        sio.stderr_print_safe(u'')
        
        #/
        exit_code = MAIN_RET_V_SHOW_ENCODING_INFO
    
    #/ 8cIUiJH
    if tmp_args_obj.show_locale_info:
        #/
        sio.stderr_write_fmt_safe(u'{}\n{:<25}{}\n{:<25}{}\n{:<25}{}\n\n',
            tt('AnRdkMS'),
            u'L10n locale hints:',
            u', '.join(SixyIO.to_u_safe(x) for x in ll_s),
            u'L10n locale:',
            SixyIO.to_u_safe(i18n.locale if i18n.locale else u''),
            u'L10n locale fb:',
            SixyIO.to_u_safe(i18n.locale_fallback if i18n.locale_fallback else u''),
        )
        
        #/
        exit_code = MAIN_RET_V_SHOW_LOCALE_INFO
    
    #/ 4iGnHUE
    if tmp_args_obj.show_locale_choices:
        sio.stderr_print_safe(tt('FZvH7zh')) 
        
        for ll in I18n.get_locale_choices(i18n_dir):
            sio.stderr_print_safe(SixyIO.fse_to_u_safe(ll)) 
        
        exit_code = MAIN_RET_V_SHOW_LOCALE_CHOICES
        
    #/ 
    if exit_code is not None:
        #/ 6ka1PPv
        return exit_code
    
    #/ 2pePlsG
    args_obj = parser.parse_args(args)
    #/ 5xFsTai
    ## exit inside |parse_args| if has errors
    
    #/
    fmt_is_de = args_obj.fmt_is_de
    ## |de| means |.desktop| file format.
    
    #/
    output_dir_path_stxt = args_obj.output_dir_path
    ## |stxt| means bytes str on Py2, unicode str on Py3.
    
    #/ 5qyicC8
    if not output_dir_path_stxt:
        output_dir_path = u''
        ## empty string works with the format at 8uZV0xm
        ##  to create a no-dir path.
    else:
        try:
            output_dir_path = sio.cae_u(output_dir_path_stxt)
        except Exception:
            #/ 9oBgE2N
            sio.stderr_print_fmt_safe(tt('F1HXaB3'), sio.cae)
            
            if sio.cae != sio.stdie:
                sio.stderr_print_fmt_safe(tt('Hvvw6GN'), sio.stdie)
            
            #/
            if debug_on:
                sio.stderr_write_tb_safe()
            
            #/ 9oBgE2N
            return MAIN_RET_V_DECODE_OUTPUT_DIR_PATH_ERR
        
        #/
        output_dir_path += u'/'
        ## |/| works with the format at 8uZV0xm to be a dir sep
        
        #/ 2cfu4Rm
        if not os.path.isdir(output_dir_path):
            #/ 6rG3A5k
            sio.stderr_print_fmt_safe(tt('BwQ2oOo'), output_dir_path)
            
            #/ 6f8eDPt
            return MAIN_RET_V_OUTPUT_DIR_NOT_EXISTING

    #/ 
    input_file_path_stxt = args_obj.input_file_path
    ## |stxt| means bytes str on Py2, unicode str on Py3.
    
    #/ 9aWIFha
    try:
        input_file_path = sio.cae_u(input_file_path_stxt)
    except Exception:
        #/ 4dKZ0v7
        sio.stderr_print_fmt_safe(tt('Bdi6LgB'), sio.cae)
        
        if sio.cae != sio.stdie:
            sio.stderr_print_fmt_safe(tt('AmypZXV'), sio.stdie)
        
        #/
        if debug_on:
            sio.stderr_write_tb_safe()
        
        #/ 4dti27r
        return MAIN_RET_V_DECODE_INPUT_FILE_PATH_ERR
    
    #/ 9j5KXCB
    try:
        input_file = sio.open_in(input_file_path)
    except Exception:
        #/ 6qC1rhv
        sio.stderr_print_fmt_safe(tt('E5U2Hm3'), input_file_path)
        
        #/
        if debug_on:
            sio.stderr_write_tb_safe()
        
        #/ 2awiFvC
        return MAIN_RET_V_OPEN_INPUT_FILE_ERR

    #/
    name_by_title = args_obj.name_by_title
    
    esc_to_space = args_obj.esc_to_space
    
    esc_to_empty = args_obj.esc_to_empty
    
    url_set = set()
    
    re_obj = re.compile(u"""<DT><A HREF="(.+?)"(.*)>(.+)</A>""")

    with input_file:
        #/ 2iWJQvK
        lines_iter = iter(input_file)
        ## Have to increment the iterator manually
        ##  so that we can catch the exception thrown by |next| below
        ##  in the nearest place. 
        
        while True:
            #/ 5kIo15P
            try:
                line = next(lines_iter, None)
                ## may raise UnicodeDecodeError if the encoding is specified wrong via cmd arg 9cCQk7p
            except UnicodeDecodeError:
                #/ 2a4z6kA
                sio.stderr_print_fmt_safe(tt('BbCyL6V'),
                    input_file_path,
                    sio.ife,
                )
                sio.stderr_print_safe(tt('D3cUHa8'))
                
                #/
                if debug_on:
                    sio.stderr_write_tb_safe()
                    
                #/ 7nftaOQ
                return MAIN_RET_V_DECODE_INPUT_FILE_LINE_ERR
            
            if line is None:
                break
            
            #/ 5hKbic4
            line = line.strip()
    
            #/ 6zlx5Ih
            match = re_obj.search(line)
    
            if not match:
                #/ 7bebbvx
                continue
    
            #/ 8zZ6fVL
            url = match.group(1)
            
            #/ 7nN0fIw
            if url in url_set:
                continue
    
            url_set.add(url)
    
            #/ 3q7Cong
            if name_by_title:
                #/ 7bzPC7Z
                output_file_name_noext = match.group(3)
            else:
                #/ 7blW9ts
                try:
                    output_file_name_noext = make_file_name_by_url(url)
                except Exception:
                    #/ 5dxuoar
                    sio.stderr_print_fmt_safe(tt('H3EQR2i'), url)
                    
                    #/
                    if debug_on:
                        sio.stderr_write_tb_safe()
                         
                    #/ 6ahxskh
                    continue
                
            #/ 4wFEmpy
            if esc_to_space or esc_to_empty:
                esc_char = u' ' if esc_to_space else u''
                
                output_file_name_noext = output_file_name_noext\
                    .replace(u'\\', esc_char)\
                    .replace(u'/', esc_char)\
                    .replace(u'<', esc_char)\
                    .replace(u'>', esc_char)\
                    .replace(u':', esc_char)\
                    .replace(u'*', esc_char)\
                    .replace(u'?', esc_char)\
                    .replace(u'"', esc_char)\
                    .replace(u'|', esc_char)
            else:
                output_file_name_noext = output_file_name_noext\
                    .replace(u'\\', u'%5C')\
                    .replace(u'/', u'%2F')\
                    .replace(u'<', u'%3C')\
                    .replace(u'>', u'%3E')\
                    .replace(u':', u'%3A')\
                    .replace(u'*', u'%2A')\
                    .replace(u'?', u'%3F')\
                    .replace(u'"', u'%22')\
                    .replace(u'|', u'%7C')
    
            #/
            if fmt_is_de:
                file_ext = u'desktop'
            else:
                file_ext = u'url'
    
            #/ 8uZV0xm
            output_file_path = sio.format(u'{}{}.{}',
                output_dir_path,
                output_file_name_noext,
                file_ext
            )
            
            #/ 7d9xdXh
            output_file_path = make_new_file_path(output_file_path)
            
            #/ 2aRIuzA
            try:
                url_file = sio.open_out(output_file_path)
            except IOError:
                #/ 5gc4T4s
                sio.stderr_print_fmt_safe(tt('DZ46vSV'), output_file_path)
                
                #/
                if debug_on:
                    sio.stderr_write_tb_safe()
                    
                #/ 9wiHC9t
                continue
            
            #/ 9gKlCPC
            try:
                with url_file:
                    if fmt_is_de:
                        #/ 2v6nYc1
                        url_file.write(u'[Desktop Entry]\n')
                        url_file.write(u'Version=1.0\n')
                        url_file.write(u'Type=Link\n')
                        url_file.write_fmt(u'URL={}\n', url)
                    else:
                        #/ 5s4H9ZS
                        url_file.write(u'[InternetShortcut]\n')
                        url_file.write_fmt(u'URL={}\n', url)
            except Exception as e:
                #/ 8nqhZvO
                sio.stderr_print_fmt_safe(tt('AfGS7Yr'), output_file_path)
                
                #/
                if debug_on:
                    sio.stderr_write_tb_safe()
                    
                #/ 3pvM2Vs
                continue
            
    #/ 2fY7Txb
    return MAIN_RET_V_OK

if __name__ == '__main__':
    sys.exit(main())
    
