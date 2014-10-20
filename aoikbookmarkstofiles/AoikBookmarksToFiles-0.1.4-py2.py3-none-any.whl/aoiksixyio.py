# coding: utf-8
"""
File ID: 8yVHVsZ
"""

import codecs
import locale
import os
import sys
import traceback

#/ define a raisex func that is compatible with both Py2 and Py3.
##
## Modified from |six|:
##  https://bitbucket.org/gutworth/six/src/cc9fce6016db076497454f9352e55b4758ccc07c/six.py?at=default#cl-632
##
## ---BEG
if sys.version_info[0] == 3:

    def raisex(tp, value, tb=None):
        if value is None:
            if isinstance(tp, BaseException):
                value = tp
            else:
                value = tp()
        if value.__traceback__ is not tb:
            raise value.with_traceback(tb)
        raise value

else:
    def exec_(_code_, _globs_=None, _locs_=None):
        """Execute code in a namespace."""
        if _globs_ is None:
            frame = sys._getframe(1)
            _globs_ = frame.f_globals
            if _locs_ is None:
                _locs_ = frame.f_locals
            del frame
        elif _locs_ is None:
            _locs_ = _globs_
        exec("""exec _code_ in _globs_, _locs_""")

    exec_("""def raisex(tp, value, tb=None):
    raise tp, value, tb
""")
## ---END

class SixyIO(object):
    
    DEBUG_ON = False
    
    IS_PY2 = sys.version_info[0] == 2
    
    #/
    _LCE = locale.getdefaultlocale()[1]
    ## stxt or None
    
    LCE = _LCE or 'utf-8'
    ## stxt
    
    #/
    _STDIE = sys.stdin.encoding
    ## stxt or None
    
    STDIE = _STDIE or LCE
    
    #/
    _STDOE = sys.stdout.encoding
    ## stxt or None
    
    STDOE = _STDOE or STDIE
    ## stxt
    
    #/
    _STDEE = sys.stderr.encoding
    ## stxt or None
    
    STDEE = _STDEE or STDIE
    ## stxt
    
    #/
    CAE = STDIE
    ## stxt
    
    BTXT_CLS = str if IS_PY2 else bytes
    UTXT_CLS = unicode if IS_PY2 else str
    
    STDEE_NOT_VALID = '5jNUcjC'
    STDOE_NOT_VALID = '2bGFZgx'
    STDIE_NOT_VALID = '8fy6R9g'
    CAE_NOT_VALID = '8dB7OzL'
    FSE_NOT_VALID = '5msQt8M'
    IFE_NOT_VALID = '3zxd6jZ'
    OFE_NOT_VALID = '9eaiwe8'
    SPIE_NOT_VALID = '5uyXWxm'
    SPOE_NOT_VALID = 'C49VtSM'
    
    TT_D = {
        STDEE_NOT_VALID: u'Error: Stderr encoding is not valid.\nPlease use env var PYTHONIOENCODING or cmd arg --stdee to specify a correct one.\n',
        STDOE_NOT_VALID: u'Error: Stdout encoding is not valid.\nPlease use env var PYTHONIOENCODING or cmd arg --stdoe to specify a correct one.\n',
        STDIE_NOT_VALID: u'Error: Stdin encoding is not valid.\nPlease use env var PYTHONIOENCODING or cmd arg --stdie to specify a correct one.\n',
        CAE_NOT_VALID: u'Error: Cmdarg encoding is not valid.\n',
        FSE_NOT_VALID: u'Error: Filesystem encoding is not valid.\n',
        IFE_NOT_VALID: u'Error: Input file encoding is not valid.\n',
        OFE_NOT_VALID: u'Error: Output file encoding is not valid.\n',
        SPIE_NOT_VALID: u'Error: Subproc input file encoding is not valid.\n',
        SPOE_NOT_VALID: u'Error: Subproc output encoding is not valid.\n',
    }
    
    FSE = sys.getfilesystemencoding() or 'utf-8'

    @staticmethod
    def get_traceback_stxt(encoding='utf-8'):
        """
        Result is (bytes) str type on Python 2 and (unicode) str type on Python 3.
        """
        #/
        exc_cls, exc_obj, tb_obj = sys.exc_info()
        
        #/
        txt_s = traceback.format_exception(exc_cls, exc_obj, tb_obj)
    
        #/
        res = ''.join(txt_s)
    
        return res
        
    @staticmethod
    def get_traceback_utxt(encoding='utf-8', errors='replace'):
        #/
        txt = SixyIO.get_traceback_stxt()
        
        #/
        if sys.version_info.major == 2:
            utxt = txt.decode(encoding, errors)
        else:
            utxt = txt
    
        #/
        return utxt
    
    @staticmethod
    def get_default_locale(self, lower=False):
        #/
        lang, encoding = locale.getdefaultlocale()
        ## can both be None
        
        #/
        if lower:
            if lang:
                lang = lang.lower()
            
            if encoding:
                encoding = encoding.lower()
                
        #/
        return lang, encoding
    
    @staticmethod
    def get_default_locale_lang(lower=False):
        return SixyIO.get_default_locale(lower=lower)[0]
    
    @staticmethod
    def get_default_locale_encoding(lower=False):
        return SixyIO.get_default_locale(lower=lower)[1]
    
    @staticmethod
    def get_native_encodings_info():
        #/
        txt_s = []
        
        txt_s.append(SixyIO.format(u'{:<25}{}', u'PYTHONIOENCODING', SixyIO.cae_to_u_safe(os.environ.get('PYTHONIOENCODING') or u'')))
        
        #/
        loc_lang, loc_encoding = locale.getdefaultlocale()
        
        txt_s.append(SixyIO.format(u'{:<25}{}', u'locale lang', SixyIO.to_u_safe(loc_lang or u'')))
        txt_s.append(SixyIO.format(u'{:<25}{}', u'locale enco', SixyIO.to_u_safe(loc_encoding or u'')))
        
        #/
        txt_s.append(SixyIO.format(u'{:<25}{}', u'stdin', SixyIO.to_u_safe(sys.stdin.encoding or u'')))
        txt_s.append(SixyIO.format(u'{:<25}{}', u'stdout', SixyIO.to_u_safe(sys.stdout.encoding or u'')))
        txt_s.append(SixyIO.format(u'{:<25}{}', u'stderr', SixyIO.to_u_safe(sys.stderr.encoding or u'')))
        
        #/
        txt_s.append(SixyIO.format(u'{:<25}{}', u'fs', SixyIO.to_u_safe(sys.getfilesystemencoding() or u'')))
        
        #/
        txt_s.append(SixyIO.format(u'{:<25}{}', u'default', SixyIO.to_u_safe(sys.getdefaultencoding() or u'')))
        
        #/
        res = u'\n'.join(txt_s)
        
        return res
    
    @staticmethod
    def encoding_is_valid(encoding):
        #/
        try:
            codecs.lookup(encoding)
            return True
        except Exception:
            return False
    
    @staticmethod
    def reload_default_encoding(encoding):
        if SixyIO.IS_PY2:
            reload(sys)
            sys.setdefaultencoding(encoding) #@UndefinedVariable
    
    @staticmethod
    def register_codec_cp65001():
        try:
            codecs.lookup('cp65001')
        except Exception:
            def lookup_func(name):
                if name.lower() == 'cp65001':
                    return codecs.lookup('utf-8')
            codecs.register(lookup_func)
    
    @staticmethod
    def register_special_codecs():
        SixyIO.register_codec_cp65001()
        
    #/   
    stdout_write_b = sys.stdout.write if IS_PY2 else sys.stdout.buffer.write
    
    @staticmethod
    def stdout_write(utxt, encoding=None, errors=None):
        #/
        if SixyIO.DEBUG_ON:
            assert SixyIO.is_u(utxt)
            
        #/
        encoding = encoding or SixyIO.STDOE
            
        errors = errors or 'strict'
        
        #/
        btxt = utxt.encode(encoding, errors)
        
        #/
        SixyIO.stdout_write_b(btxt)
        
    @staticmethod
    def stdout_print(utxt, encoding=None, errors=None):
        SixyIO.stdout_write(utxt, encoding=encoding, errors=errors)
        SixyIO.stdout_write(u'\n', encoding=encoding, errors=errors)
        
    @staticmethod
    def stdout_write_safe(utxt, encoding=None, errors=None):
        #/
        errors = errors or 'replace'
        
        #/
        SixyIO.stdout_write(utxt, encoding=encoding, errors=errors)
        
    @staticmethod
    def stdout_print_safe(utxt, encoding=None, errors=None):
        #/
        errors = errors or 'replace'
        
        #/
        SixyIO.stdout_write(utxt, encoding=encoding, errors=errors)
        SixyIO.stdout_write(u'\n', encoding=encoding, errors=errors)
        
    @staticmethod
    def stdout_write_fmt(fmt, *args, **kwargs):
        #/
        _encoding = kwargs.pop('_encoding', None)
        
        _errors = kwargs.pop('_errors', None)
        
        #/
        utxt = SixyIO.format(fmt, *args, **kwargs)
        
        #/
        SixyIO.stdout_write(utxt, encoding=_encoding, errors=_errors)
        
    @staticmethod
    def stdout_print_fmt(fmt, *args, **kwargs):
        #/
        _encoding = kwargs.pop('_encoding', None)
        
        _errors = kwargs.pop('_errors', None)
        
        #/
        utxt = SixyIO.format(fmt, *args, **kwargs)
        
        #/
        SixyIO.stdout_write(utxt, encoding=_encoding, errors=_errors)
        SixyIO.stdout_write(u'\n', encoding=_encoding, errors=_errors)
        
    @staticmethod
    def stdout_write_fmt_safe(fmt, *args, **kwargs):
        #/
        kwargs.setdefault('_errors', 'replace')
        
        #/
        SixyIO.stdout_write_fmt(fmt, *args, **kwargs)
        
    @staticmethod
    def stdout_print_fmt_safe(fmt, *args, **kwargs):
        #/
        kwargs.setdefault('_errors', 'replace')
        
        #/
        SixyIO.stdout_print_fmt(fmt, *args, **kwargs)
    
    @staticmethod
    def stdout_write_tb_safe(utxt=None, fmt=None, encoding=None):
        #/
        if SixyIO.DEBUG_ON:
            assert utxt is None or SixyIO.is_u(utxt)
        
            assert fmt is None or SixyIO.is_u(fmt)
        
        #/
        utxt = utxt or u''
        
        #/
        fmt = fmt or u'{}---\n{}---\n'
        
        #/
        tb_utxt = SixyIO.get_traceback_utxt()
        
        #/
        res_utxt = fmt.format(utxt, tb_utxt)
        
        #/
        SixyIO.stdout_write_safe(res_utxt, encoding=encoding)
        
    @staticmethod
    def stdout_make_writer(encoding=None, errors=None):
        #/
        encoding = encoding or SixyIO.STDOE
        
        errors = errors or 'strict'
        
        #/
        buf = sys.stdout if SixyIO.IS_PY2 else sys.stdout.buffer
        
        #/
        return codecs.getwriter(encoding)(buf, errors)
    
    #/
    stderr_write_b = sys.stderr.write if IS_PY2 else sys.stderr.buffer.write
        
    @staticmethod
    def stderr_write(utxt, encoding=None, errors=None):
        #/
        if SixyIO.DEBUG_ON:
            assert SixyIO.is_u(utxt)
            
        #/
        encoding = encoding or SixyIO.STDEE
            
        errors = errors or 'strict'
        
        #/
        btxt = utxt.encode(encoding, errors)
        
        #/
        SixyIO.stderr_write_b(btxt)
        
    @staticmethod
    def stderr_print(utxt, encoding=None, errors=None):
        SixyIO.stderr_write(utxt, encoding=encoding, errors=errors)
        SixyIO.stderr_write(u'\n', encoding=encoding, errors=errors)
        
    @staticmethod
    def stderr_write_safe(utxt, encoding=None, errors=None):
        #/
        errors = errors or 'replace'
        
        #/
        SixyIO.stderr_write(utxt, encoding=encoding, errors=errors)
        
    @staticmethod
    def stderr_print_safe(utxt, encoding=None, errors=None):
        #/
        errors = errors or 'replace'
        
        #/
        SixyIO.stderr_write(utxt, encoding=encoding, errors=errors)
        SixyIO.stderr_write(u'\n', encoding=encoding, errors=errors)
        
    @staticmethod
    def stderr_write_fmt(fmt, *args, **kwargs):
        #/
        _encoding = kwargs.pop('_encoding', None)
        
        _errors = kwargs.pop('_errors', None)
        
        #/
        utxt = SixyIO.format(fmt, *args, **kwargs)
        
        #/
        SixyIO.stderr_write(utxt, encoding=_encoding, errors=_errors)
        
    @staticmethod
    def stderr_print_fmt(fmt, *args, **kwargs):
        #/
        _encoding = kwargs.pop('_encoding', None)
        
        _errors = kwargs.pop('_errors', None)
        
        #/
        utxt = SixyIO.format(fmt, *args, **kwargs)
        
        #/
        SixyIO.stderr_write(utxt, encoding=_encoding, errors=_errors)
        SixyIO.stderr_write(u'\n', encoding=_encoding, errors=_errors)
        
    @staticmethod
    def stderr_write_fmt_safe(fmt, *args, **kwargs):
        #/
        kwargs.setdefault('_errors', 'replace')
        
        #/
        SixyIO.stderr_write_fmt(fmt, *args, **kwargs)
        
    @staticmethod
    def stderr_print_fmt_safe(fmt, *args, **kwargs):
        #/
        kwargs.setdefault('_errors', 'replace')
        
        #/
        SixyIO.stderr_print_fmt(fmt, *args, **kwargs)
    
    @staticmethod
    def stderr_write_tb_safe(utxt=None, fmt=None, encoding=None):
        #/
        if SixyIO.DEBUG_ON:
            assert utxt is None or SixyIO.is_u(utxt)
        
            assert fmt is None or SixyIO.is_u(fmt)
        
        #/
        utxt = utxt or u''
        
        #/
        fmt = fmt or u'{}---\n{}---\n'
        
        #/
        tb_utxt = SixyIO.get_traceback_utxt()
        
        #/
        res_utxt = fmt.format(utxt, tb_utxt)
        
        #/
        SixyIO.stderr_write_safe(res_utxt, encoding=encoding)
        
    @staticmethod
    def stderr_make_writer(encoding=None, errors=None):
        #/
        encoding = encoding or SixyIO.STDEE
        
        errors = errors or 'strict'
        
        #/
        buf = sys.stderr if SixyIO.IS_PY2 else sys.stderr.buffer
        
        #/
        return codecs.getwriter(encoding)(buf, errors)
    
    @staticmethod
    def to_b(txt, encoding=None, errors=None):
        #/
        encoding = encoding or 'utf-8'
        
        #/
        errors = errors or 'strict'
        
        #/
        if isinstance(txt, SixyIO.UTXT_CLS):
            res = txt.encode(encoding, errors)
        elif isinstance(txt, SixyIO.BTXT_CLS):
            res = txt
        else:
            assert False
        
        return res
    
    @staticmethod
    def to_b_safe(txt, encoding=None, errors=None):
        #/
        errors = errors or 'replace'
            
        #/
        return SixyIO.to_b(txt=txt, encoding=encoding, errors=errors)
    
    @staticmethod
    def to_str(obj, encoding=None, errors=None):
        #/
        if encoding is None:
            encoding = 'utf-8'
        
        #/
        if errors is None:
            errors = 'strict'
        
        #/
        if SixyIO.IS_PY2:
            if isinstance(obj, str):
                res = obj
            elif isinstance(obj, unicode):
                res = obj.decode(encoding, errors)
            else:
                res = str(obj)
        else:
            if isinstance(obj, str):
                res = obj
            else:
                res = str(obj)
        
        return res
    
    @staticmethod
    def to_str_safe(obj, encoding=None, errors=None):
        #/
        errors = errors or 'replace'
            
        #/
        return SixyIO.to_str(obj=obj, encoding=encoding, errors=errors)
        
    @staticmethod
    def is_u(obj):
        if SixyIO.IS_PY2:
            unicode_cls = unicode
        else:
            unicode_cls = str
        
        return isinstance(obj, unicode_cls)
    
    @staticmethod
    def to_u(obj, encoding=None, errors=None):
        #/
        encoding = encoding or 'utf-8'
        
        errors = errors or 'strict'
        
        #/
        if isinstance(obj, SixyIO.UTXT_CLS):
            res = obj
        elif isinstance(obj, SixyIO.BTXT_CLS):
            res = SixyIO.UTXT_CLS(obj, encoding=encoding, errors=errors)
        else:
            res = SixyIO.UTXT_CLS(obj)
        
        return res
        
    @staticmethod
    def to_u_safe(obj, encoding=None, errors=None):
        #/
        errors = errors or 'replace'
        
        #/
        return SixyIO.to_u(obj, encoding, errors)
        
    @staticmethod
    def cae_to_u(txt, encoding=None, errors=None):
        #/
        encoding = encoding or SixyIO.CAE
        
        #/
        return SixyIO.to_u(txt, encoding=encoding, errors=errors)
        
    @staticmethod
    def cae_to_u_safe(txt, encoding=None, errors=None):
        #/
        encoding = encoding or SixyIO.CAE
        
        errors = errors or 'replace'
        
        #/
        return SixyIO.to_u(txt, encoding=encoding, errors=errors)
        
    @staticmethod
    def fse_to_u(txt, encoding=None, errors=None):
        #/
        encoding = encoding or SixyIO.FSE
        
        #/
        return SixyIO.to_u(txt, encoding=encoding, errors=errors)
        
    @staticmethod
    def fse_to_u_safe(txt, encoding=None, errors=None):
        #/
        encoding = encoding or SixyIO.FSE
        
        errors = errors or 'replace'
        
        #/
        return SixyIO.to_u(txt, errors=errors)
        
    @staticmethod
    def format(fmt, *args, **kwargs):
        #/
        if SixyIO.DEBUG_ON:
            assert SixyIO.is_u(fmt)
        
            if args:
                for arg in args:
                    assert SixyIO.is_u(arg)
            
            if kwargs:
                for key, val in kwargs.items():
                    assert SixyIO.is_u(key)
                    assert SixyIO.is_u(val)
        
        #/
        txt = fmt.format(*args, **kwargs)
        
        return txt
    
    @staticmethod
    def open(filename, mode, **kwargs):
        #/
        assert SixyIO.is_u(filename)
        
        #/
        return codecs.open(filename, mode, **kwargs)
    
class FileForceWriteUnicodeWrapper(object):
    
    def __init__(self, file_obj, debug_on):
        self.file = file_obj
        self.debug_on = debug_on
                
    def __getattr__(self, name):
        return getattr(self.file, name)
    
    def __enter__(self, *args, **kwargs):
        """
        __enter__ is special that __getattr__ does not cover
        """
        return self.file.__enter__(*args, **kwargs)

    def __exit__(self, *args, **kwargs):
        """
        __exit__ is special that __getattr__ does not cover
        """
        return self.file.__exit__(*args, **kwargs)
     
    def write(self, txt):
        #/
        if self.debug_on:
            assert SixyIO.is_u(txt)
        
        #/
        return self.file.write(txt)
     
    def write_fmt(self, fmt, *args, **kwargs):
        #/
        if self.debug_on:
            assert SixyIO.is_u(fmt)
        
            if args:
                for arg in args:
                    assert SixyIO.is_u(arg)
            
            if kwargs:
                for key, val in kwargs.items():
                    assert SixyIO.is_u(key)
                    assert SixyIO.is_u(val)
                    
        #/
        if not args and not kwargs:
            txt = fmt
        else:
            txt = fmt.format(*args, **kwargs)
        
        #/
        return self.file.write(txt)
    
class SixyIOObj(object):
            
    def __init__(self,
        stdioe=None,
        stdie=None,
        stdoe=None,
        stdee=None,
        cae=None,
        fse=None,
        ife=None,
        ofe=None,
        spie=None,
        spoe=None,
        exit_code=None,
        tt=None,
        debug_on=False,
    ):
        """
        stdie: Stdin encoding. By default: stdie or stdioe or SixyIO.STDIE
        stdoe: Stdout encoding. By default: stdoe or stdioe or SixyIO.STDOE
        stdee: Stderr encoding. By default: stdee or stdioe or SixyIO.STDEE
        cae: command argument encoding. By default: cae or SixyIO.CAE
        fse: filesystem encoding. By default: fse or SixyIO.FSE
        ife: input file encoding. By default utf-8
        ofe: output file encoding. By default utf-8
        spie: subproc input encoding. By default utf-8
        spoe: subproc output encoding. By default utf-8
        exit_code: exit code on init error. If none, raise exception instead of exit. 
        """
        #/
        self.exit_code = exit_code
        
        #/
        self.debug_on = debug_on
        
        if self.debug_on is None:
            self.debug_on = SixyIO.DEBUG_ON
            
        #/
        if tt is None:
            def tt(key):
                return SixyIO.TT_D[key]
        
        #/
        self.stdee = stdee or stdioe or SixyIO.STDEE
            
        assert self.stdee
        
        #/
        try:
            self.stdee = SixyIO.to_u(self.stdee)
            
            assert SixyIO.encoding_is_valid(self.stdee)
        except Exception as e:
            #/ 6xW0Tns
            msg = tt(SixyIO.STDEE_NOT_VALID)
            
            #/
            if exit_code is None:
                raisex(AssertionError(SixyIO.STDEE_NOT_VALID, msg, e), None, sys.exc_info()[2])
            
            #/
            SixyIO.stderr_write_tb_safe(msg, encoding=SixyIO.STDEE)
            ## |self.stdee| is not valid so use |SixyIO.STDEE| as fallback.
            
            #/
            sys.exit(self.exit_code)
                
        assert SixyIO.is_u(self.stdee)
        
        #/
        self.stdoe = stdoe or stdioe or SixyIO.STDOE
            
        assert self.stdoe
        
        #/
        try:
            self.stdoe = SixyIO.to_u(self.stdoe)
            
            assert SixyIO.encoding_is_valid(self.stdoe)
        except Exception as e:
            #/
            msg = tt(SixyIO.STDOE_NOT_VALID)
            
            #/
            if exit_code is None:
                raisex(AssertionError(SixyIO.STDOE_NOT_VALID, msg, e), None, sys.exc_info()[2])
            
            #/
            SixyIO.stderr_write_tb_safe(msg, encoding=self.stdee)
            
            #/
            sys.exit(self.exit_code)
                
        assert SixyIO.is_u(self.stdoe)
        
        #/
        self.stdie = stdie or stdioe or SixyIO.STDIE
            
        assert self.stdie
        
        #/
        try:
            self.stdie = SixyIO.to_u(self.stdie)
            
            assert SixyIO.encoding_is_valid(self.stdie)
        except Exception as e:
            #/
            msg = tt(SixyIO.STDIE_NOT_VALID)
            
            #/
            if exit_code is None:
                raisex(AssertionError(SixyIO.STDIE_NOT_VALID, msg, e), None, sys.exc_info()[2])
            
            #/
            SixyIO.stderr_write_tb_safe(msg, encoding=self.stdee)
            
            #/
            sys.exit(self.exit_code)
                
        assert SixyIO.is_u(self.stdie)
        
        #/
        self.cae = cae or SixyIO.CAE
        
        assert self.cae
        
        #/
        try:
            self.cae = SixyIO.to_u(self.cae)
            
            assert SixyIO.encoding_is_valid(self.cae)
        except Exception as e:
            #/
            msg = tt(SixyIO.CAE_NOT_VALID)
            
            #/
            if exit_code is None:
                raisex(AssertionError(SixyIO.CAE_NOT_VALID, msg, e), None, sys.exc_info()[2])
            
            #/
            SixyIO.stderr_write_tb_safe(msg, encoding=self.stdee)
            
            #/
            sys.exit(self.exit_code)
                
        assert SixyIO.is_u(self.cae)
        
        
        #/
        self.fse = fse or SixyIO.FSE
            
        assert self.fse
        
        #/
        try:
            self.fse = SixyIO.to_u(self.fse)
            
            assert SixyIO.encoding_is_valid(self.fse)
        except Exception as e:
            #/
            msg = tt(SixyIO.FSE_NOT_VALID)
            
            #/
            if exit_code is None:
                raisex(AssertionError(SixyIO.FSE_NOT_VALID, msg, e), None, sys.exc_info()[2])
            
            #/
            SixyIO.stderr_write_tb_safe(msg, encoding=self.stdee)
            
            #/
            sys.exit(self.exit_code)
                
        assert SixyIO.is_u(self.fse)
        
        #/
        self.ife = ife
        
        if not self.ife:
            self.ife = 'utf-8'
        
        #/
        try:
            self.ife = SixyIO.to_u(self.ife)
            
            assert SixyIO.encoding_is_valid(self.ife)
        except Exception as e:
            #/
            msg = tt(SixyIO.IFE_NOT_VALID)
            
            #/
            if exit_code is None:
                raisex(AssertionError(SixyIO.IFE_NOT_VALID, msg, e), None, sys.exc_info()[2])
            
            #/
            SixyIO.stderr_write_tb_safe(msg, encoding=self.stdee)
            
            #/
            sys.exit(self.exit_code)
                
        assert SixyIO.is_u(self.ife)
        
        #/
        self.ofe = ofe
        
        if not self.ofe:
            self.ofe = 'utf-8'
        
        #/
        try:
            self.ofe = SixyIO.to_u(self.ofe)
            
            assert SixyIO.encoding_is_valid(self.ofe)
        except Exception as e:
            #/
            msg = tt(SixyIO.OFE_NOT_VALID)
            
            #/
            if exit_code is None:
                raisex(AssertionError(SixyIO.OFE_NOT_VALID, msg, e), None, sys.exc_info()[2])
            
            #/
            SixyIO.stderr_write_tb_safe(msg, encoding=self.stdee)
            
            #/
            sys.exit(self.exit_code)
                
        assert SixyIO.is_u(self.ofe)
        
        #/
        self.spie = spie
        
        if not self.spie:
            self.spie = 'utf-8'
            
        assert self.spie
        
        #/
        try:
            self.spie = SixyIO.to_u(self.spie)
            
            assert SixyIO.encoding_is_valid(self.spie)
        except Exception as e:
            #/
            msg = tt(SixyIO.SPIE_NOT_VALID)
            
            #/
            if exit_code is None:
                raisex(AssertionError(SixyIO.SPIE_NOT_VALID, msg, e), None, sys.exc_info()[2])
            
            #/
            SixyIO.stderr_write_tb_safe(msg, encoding=self.stdee)
            
            #/
            sys.exit(self.exit_code)
                
        assert SixyIO.is_u(self.spie)
        
        #/
        self.spoe = spoe
        
        if not self.spoe:
            self.spoe = 'utf-8'
            
        assert self.spoe
        
        #/
        try:
            self.spoe = SixyIO.to_u(self.spoe)
            
            assert SixyIO.encoding_is_valid(self.spoe)
        except Exception as e:
            #/
            msg = tt(SixyIO.SPOE_NOT_VALID)
            
            #/
            if exit_code is None:
                raisex(AssertionError(SixyIO.SPOE_NOT_VALID, msg, e), None, sys.exc_info()[2])
            
            #/
            SixyIO.stderr_write_tb_safe(msg, encoding=self.stdee)
            
            #/
            sys.exit(self.exit_code)
                
        assert SixyIO.is_u(self.spoe)
            
    def __str__(self):
        #/
        res = self.__unicode__()
        
        #/
        if SixyIO.IS_PY2:
            res = res.encode('utf-8', 'replace')
            
        #/
        return res
            
    def __unicode__(self):
        return self.get_sixyio_encodings_info()
            
    def __repr__(self):
        return self.__str__()
    
    def get_sixyio_encodings_info(self):
        return u"""%-25s%s
%-25s%s
%-25s%s
%-25s%s
%-25s%s
%-25s%s
%-25s%s
%-25s%s
%-25s%s""" % (
       u"stdin:", self.stdie,
       u"stdout:", self.stdoe,
       u"stderr:", self.stdee,
       u"cae:", self.cae, 
       u"fse:", self.fse,
       u"ife:", self.ife,
       u"ofe:", self.ofe,
       u"spie:", self.spie,
       u"spoe:", self.spoe,
       )

    def stdout_write(self, utxt, encoding=None, errors=None):
        #/
        encoding = encoding or self.stdoe 
        
        #/
        SixyIO.stdout_write(utxt, encoding=encoding, errors=errors)
        
    def stdout_print(self, utxt, encoding=None, errors=None):
        #/
        encoding = encoding or self.stdoe 
        
        #/
        SixyIO.stdout_print(utxt, encoding=encoding, errors=errors)
        
    def stdout_write_safe(self, utxt, encoding=None, errors=None):
        #/
        encoding = encoding or self.stdoe 
        
        #/
        SixyIO.stdout_write_safe(utxt, encoding=encoding, errors=errors)
        
    def stdout_print_safe(self, utxt, encoding=None, errors=None):
        #/
        encoding = encoding or self.stdoe 
        
        #/
        SixyIO.stdout_print_safe(utxt, encoding=encoding, errors=errors)
        
    def stdout_write_fmt(self, fmt, *args, **kwargs):
        #/
        kwargs.setdefault('_encoding', self.stdoe)
        
        #/
        SixyIO.stdout_write_fmt(fmt, *args, **kwargs)
        
    def stdout_print_fmt(self, fmt, *args, **kwargs):
        #/
        kwargs.setdefault('_encoding', self.stdoe)
        
        #/
        SixyIO.stdout_print_fmt(fmt, *args, **kwargs)
        
    def stdout_write_fmt_safe(self, fmt, *args, **kwargs):
        #/
        kwargs.setdefault('_encoding', self.stdoe)
        
        #/
        SixyIO.stdout_write_fmt_safe(fmt, *args, **kwargs)
        
    def stdout_print_fmt_safe(self, fmt, *args, **kwargs):
        #/
        kwargs.setdefault('_encoding', self.stdoe)
        
        #/
        SixyIO.stdout_print_fmt_safe(fmt, *args, **kwargs)
    
    def stdout_write_tb_safe(self, utxt=None, fmt=None, encoding=None):
        #/
        encoding = encoding or self.stdoe
        
        #/
        SixyIO.stdout_write_tb_safe(utxt, fmt=fmt, encoding=encoding)
    
    def stdout_make_writer(self, encoding=None, errors=None):
        #/
        encoding = encoding or self.stdoe
        
        #/
        return SixyIO.stdout_make_writer(encoding=encoding, errors=errors)

    def stderr_write(self, utxt, encoding=None, errors=None):
        #/
        encoding = encoding or self.stdee 
        
        #/
        SixyIO.stderr_write(utxt, encoding=encoding, errors=errors)
        
    def stderr_print(self, utxt, encoding=None, errors=None):
        #/
        encoding = encoding or self.stdee 
        
        #/
        SixyIO.stderr_print(utxt, encoding=encoding, errors=errors)
        
    def stderr_write_safe(self, utxt, encoding=None, errors=None):
        #/
        encoding = encoding or self.stdee 
        
        #/
        SixyIO.stderr_write_safe(utxt, encoding=encoding, errors=errors)
        
    def stderr_print_safe(self, utxt, encoding=None, errors=None):
        #/
        encoding = encoding or self.stdee 
        
        #/
        SixyIO.stderr_print_safe(utxt, encoding=encoding, errors=errors)
        
    def stderr_write_fmt(self, fmt, *args, **kwargs):
        #/
        kwargs.setdefault('_encoding', self.stdee)
        
        #/
        SixyIO.stderr_write_fmt(fmt, *args, **kwargs)
        
    def stderr_print_fmt(self, fmt, *args, **kwargs):
        #/
        kwargs.setdefault('_encoding', self.stdee)
        
        #/
        SixyIO.stderr_print_fmt(fmt, *args, **kwargs)
        
    def stderr_write_fmt_safe(self, fmt, *args, **kwargs):
        #/
        kwargs.setdefault('_encoding', self.stdee)
        
        #/
        SixyIO.stderr_write_fmt_safe(fmt, *args, **kwargs)
        
    def stderr_print_fmt_safe(self, fmt, *args, **kwargs):
        #/
        kwargs.setdefault('_encoding', self.stdee)
        
        #/
        SixyIO.stderr_print_fmt_safe(fmt, *args, **kwargs)
    
    def stderr_write_tb_safe(self, utxt=None, fmt=None, encoding=None):
        #/
        encoding = encoding or self.stdee
        
        #/
        SixyIO.stderr_write_tb_safe(utxt, fmt=fmt, encoding=encoding)
    
    def stderr_make_writer(self, encoding=None, errors=None):
        #/
        encoding = encoding or self.stdee
        
        #/
        return SixyIO.stderr_make_writer(encoding=encoding, errors=errors)
        
    def cae_to_u(self, txt, encoding=None, errors=None):
        #/
        encoding = encoding or self.cae
        
        #/
        return SixyIO.cae_to_u(txt, encoding=encoding, errors=errors)
            
    def cae_to_u_safe(self, txt, encoding=None, errors=None):
        #/
        encoding = encoding or self.cae
        
        #/
        return SixyIO.cae_to_u_safe(txt, encoding=encoding, errors=errors)
        
    def fse_to_u(self, txt, encoding=None, errors=None):
        #/
        encoding = encoding or self.fse
        
        #/
        return SixyIO.fse_to_u(txt, encoding=encoding, errors=errors)
        
    def fse_to_u_safe(self, txt, encoding=None, errors=None):
        #/
        encoding = encoding or self.fse
        
        #/
        return SixyIO.fse_to_u_safe(txt, encoding=encoding, errors=errors)
    
    def open_in(self, filename, mode=u'r', **kwargs):
        #/
        assert SixyIO.is_u(filename)
        
        #/
        return codecs.open(filename, mode, self.ife, **kwargs)
    
    def open_out(self, filename, mode=u'w', **kwargs):
        #/
        assert SixyIO.is_u(filename)
        
        #/
        file_obj = codecs.open(filename, mode, self.ofe, **kwargs)
        
        #/
        file_obj = FileForceWriteUnicodeWrapper(file_obj, debug_on=self.debug_on)
        
        #/
        return file_obj
