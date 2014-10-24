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

    def raisex(tp, value=None, tb=None):
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

    exec_("""def raisex(tp, value=None, tb=None):
    raise tp, value, tb
""")
## ---END

class SixyIO(object):
    
    #/
    DEBUG_ON = False
    
    #/
    IS_PY2 = sys.version_info[0] == 2
    
    #/
    BTXT_CLS = str if IS_PY2 else bytes
    
    UTXT_CLS = unicode if IS_PY2 else str
    
    #/
    _LCE = locale.getdefaultlocale()[1]
    ## stxt or None
    
    LCE = _LCE or 'utf-8'
    ## stxt

    LCE_UTXT = LCE.decode('ascii', 'replace') if IS_PY2 else LCE
    
    #/
    _STDIE = sys.stdin.encoding
    ## stxt or None
    
    STDIE = _STDIE or LCE

    STDIE_UTXT = STDIE.decode('ascii', 'replace') if IS_PY2 else STDIE
    
    #/
    _STDOE = sys.stdout.encoding
    ## stxt or None
    
    STDOE = _STDOE or STDIE
    ## stxt

    STDOE_UTXT = STDOE.decode('ascii', 'replace') if IS_PY2 else STDOE
    
    #/
    _STDEE = sys.stderr.encoding
    ## stxt or None
    
    STDEE = _STDEE or STDIE
    ## stxt

    STDEE_UTXT = STDEE.decode('ascii', 'replace') if IS_PY2 else STDEE
    
    #/
    CAE = STDIE
    ## stxt

    CAE_UTXT = CAE.decode('ascii', 'replace') if IS_PY2 else CAE
    
    FSE = sys.getfilesystemencoding() or 'utf-8'
    
    FSE_UTXT = FSE.decode('ascii', 'replace') if IS_PY2 else FSE
    
    IFE = 'utf-8'
    
    IFE_UTXT = IFE.decode('ascii', 'replace') if IS_PY2 else IFE
    
    OFE = 'utf-8'
    
    OFE_UTXT = OFE.decode('ascii', 'replace') if IS_PY2 else OFE
    
    SPCE = 'utf-8'
    
    SPCE_UTXT = SPCE.decode('ascii', 'replace') if IS_PY2 else SPCE
    
    SPIE = 'utf-8'
    
    SPIE_UTXT = SPIE.decode('ascii', 'replace') if IS_PY2 else SPIE
    
    SPOE = 'utf-8'
    
    SPOE_UTXT = SPOE.decode('ascii', 'replace') if IS_PY2 else SPOE
    
    SPEE = 'utf-8'
    
    SPEE_UTXT = SPEE.decode('ascii', 'replace') if IS_PY2 else SPEE
    
    SIXYIO_CLS_NOT_ALLOW_CREATING_OBJ = '9gwa3bx'
    STDEE_NOT_VALID = '5jNUcjC'
    STDOE_NOT_VALID = '2bGFZgx'
    STDIE_NOT_VALID = '8fy6R9g'
    CAE_NOT_VALID = '8dB7OzL'
    FSE_NOT_VALID = '5msQt8M'
    IFE_NOT_VALID = '3zxd6jZ'
    OFE_NOT_VALID = '9eaiwe8'
    SPCE_NOT_VALID = '8dcQynl'
    SPIE_NOT_VALID = '5uyXWxm'
    SPOE_NOT_VALID = 'C49VtSM'
    SPEE_NOT_VALID = 'GmH4cDl'
    
    TT_D = {
        STDEE_NOT_VALID: u'Error: Stderr encoding is not valid.\nEncoding is |{}|.\nPlease use env var |PYTHONIOENCODING| or cmd arg |--stdee| to specify a correct one.\n',
        STDOE_NOT_VALID: u'Error: Stdout encoding is not valid.\nEncoding is |{}|.\nPlease use env var |PYTHONIOENCODING| or cmd arg |--stdoe| to specify a correct one.\n',
        STDIE_NOT_VALID: u'Error: Stdin encoding is not valid.\nEncoding is |{}|.\nPlease use env var |PYTHONIOENCODING| or cmd arg |--stdie| to specify a correct one.\n',
        CAE_NOT_VALID: u'Error: Cmdarg encoding is not valid.\nEncoding is |{}|.\n',
        FSE_NOT_VALID: u'Error: Filesystem encoding is not valid.\nEncoding is |{}|.\n',
        IFE_NOT_VALID: u'Error: Input file encoding is not valid.\nEncoding is |{}|.\n',
        OFE_NOT_VALID: u'Error: Output file encoding is not valid.\nEncoding is |{}|.\n',
        SPCE_NOT_VALID: u'Error: Subproc command encoding is not valid.\nEncoding is |{}|.\n',
        SPIE_NOT_VALID: u'Error: Subproc stdin encoding is not valid.\nEncoding is |{}|.\n',
        SPOE_NOT_VALID: u'Error: Subproc stdout encoding is not valid.\nEncoding is |{}|.\n',
        SPEE_NOT_VALID: u'Error: Subproc stderr encoding is not valid.\nEncoding is |{}|.\n',
    }
    
    def __init__(self):
        msg = u'Can not create object of class SixyIO. Use class SixyIOObj instead.'
        
        raisex(AssertionError(SixyIO.SIXYIO_CLS_NOT_ALLOW_CREATING_OBJ, msg))
    
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
        
    @staticmethod
    def stdin_make_reader(encoding=None, errors=None):
        #/
        encoding = encoding or SixyIO.STDIE
        
        errors = errors or 'strict'
        
        #/
        buf = sys.stdin if SixyIO.IS_PY2 else sys.stdin.buffer
        
        #/
        reader = codecs.getreader(encoding)(buf, errors)
        
        return reader
        
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
        return SixyIO.to_u(obj, encoding=encoding, errors=errors)
    
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
        return SixyIO.to_u(txt, encoding=encoding, errors=errors)

    @staticmethod
    def spce_to_b(txt, encoding=None, errors=None):
        #/
        encoding = encoding or SixyIO.SPCE
        
        #/
        return SixyIO.to_b(txt, encoding=encoding, errors=errors)
        
    @staticmethod
    def spce_to_b_safe(txt, encoding=None, errors=None):
        #/
        encoding = encoding or SixyIO.SPCE
        
        errors = errors or 'replace'
        
        #/
        return SixyIO.to_b(txt, encoding=encoding, errors=errors)

    @staticmethod
    def spie_to_b(txt, encoding=None, errors=None):
        #/
        encoding = encoding or SixyIO.SPIE
        
        #/
        return SixyIO.to_b(txt, encoding=encoding, errors=errors)
        
    @staticmethod
    def spie_to_b_safe(txt, encoding=None, errors=None):
        #/
        encoding = encoding or SixyIO.SPIE
        
        errors = errors or 'replace'
        
        #/
        return SixyIO.to_b(txt, encoding=encoding, errors=errors)
    
    @staticmethod
    def spoe_to_u(txt, encoding=None, errors=None):
        #/
        encoding = encoding or SixyIO.SPOE
        
        #/
        return SixyIO.to_u(txt, encoding=encoding, errors=errors)
        
    @staticmethod
    def spoe_to_u_safe(txt, encoding=None, errors=None):
        #/
        encoding = encoding or SixyIO.SPOE
        
        errors = errors or 'replace'
        
        #/
        return SixyIO.to_u(txt, encoding=encoding, errors=errors)
    
    @staticmethod
    def spee_to_u(txt, encoding=None, errors=None):
        #/
        encoding = encoding or SixyIO.SPEE
        
        #/
        return SixyIO.to_u(txt, encoding=encoding, errors=errors)
        
    @staticmethod
    def spee_to_u_safe(txt, encoding=None, errors=None):
        #/
        encoding = encoding or SixyIO.SPEE
        
        errors = errors or 'replace'
        
        #/
        return SixyIO.to_u(txt, encoding=encoding, errors=errors)
    
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
        spce=None,
        spie=None,
        spoe=None,
        spee=None,
        exit_code=None,
        tt=None,
        debug_on=False,
    ):
        """
        stdie: Stdin encoding.
        stdoe: Stdout encoding.
        stdee: Stderr encoding.
        cae: Command argument encoding.
        fse: Filesystem encoding.
        ife: Input file encoding.
        ofe: Output file encoding.
        spce: Subproc command encoding.
        spie: Subproc stdin encoding.
        spoe: Subproc stdout encoding.
        spee: Subproc stderr encoding.
        exit_code: Exit code on init error. If none, raise exception instead of exit. 
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
        
        self.stdee_utxt = SixyIO.to_u_safe(self.stdee, encoding='ascii')
        
        #/
        if not SixyIO.encoding_is_valid(self.stdee):
            #/ 6xW0Tns
            msg = SixyIO.format(tt(SixyIO.STDEE_NOT_VALID), self.stdee_utxt)
            
            #/
            if exit_code is None:
                raisex(AssertionError(SixyIO.STDEE_NOT_VALID, msg))
            
            #/
            SixyIO.stderr_write_tb_safe(msg, encoding=SixyIO.STDEE)
            ## |self.stdee| is not valid so use |SixyIO.STDEE| as fallback.
            
            #/
            sys.exit(self.exit_code)
        
        #/
        self.stdoe = stdoe or stdioe or SixyIO.STDOE
            
        assert self.stdoe
        
        self.stdoe_utxt = SixyIO.to_u_safe(self.stdoe, encoding='ascii')
        
        #/
        if not SixyIO.encoding_is_valid(self.stdoe):
            #/
            msg = SixyIO.format(tt(SixyIO.STDOE_NOT_VALID), self.stdoe_utxt)
            
            #/
            if exit_code is None:
                raisex(AssertionError(SixyIO.STDOE_NOT_VALID, msg))
            
            #/
            SixyIO.stderr_write_safe(msg, encoding=self.stdee)
            
            #/
            sys.exit(self.exit_code)
        
        #/
        self.stdie = stdie or stdioe or SixyIO.STDIE
            
        assert self.stdie
        
        self.stdie_utxt = SixyIO.to_u_safe(self.stdie, encoding='ascii')
        
        #/
        if not SixyIO.encoding_is_valid(self.stdie):
            #/
            msg = SixyIO.format(tt(SixyIO.STDIE_NOT_VALID), self.stdie_utxt)
            
            #/
            if exit_code is None:
                raisex(AssertionError(SixyIO.STDIE_NOT_VALID, msg))
            
            #/
            SixyIO.stderr_write_safe(msg, encoding=self.stdee)
            
            #/
            sys.exit(self.exit_code)
        
        #/
        self.cae = cae or SixyIO.CAE
        
        assert self.cae
        
        self.cae_utxt = SixyIO.to_u_safe(self.cae, encoding='ascii')
        
        #/
        if not SixyIO.encoding_is_valid(self.cae):
            #/
            msg = SixyIO.format(tt(SixyIO.CAE_NOT_VALID), self.cae_utxt)
            
            #/
            if exit_code is None:
                raisex(AssertionError(SixyIO.CAE_NOT_VALID, msg))
            
            #/
            SixyIO.stderr_write_safe(msg, encoding=self.stdee)
            
            #/
            sys.exit(self.exit_code)
        
        #/
        self.fse = fse or SixyIO.FSE
            
        assert self.fse
        
        self.fse_utxt = SixyIO.to_u_safe(self.fse, encoding='ascii')
        
        #/
        if not SixyIO.encoding_is_valid(self.fse):
            #/
            msg = SixyIO.format(tt(SixyIO.FSE_NOT_VALID), self.fse_utxt)
            
            #/
            if exit_code is None:
                raisex(AssertionError(SixyIO.FSE_NOT_VALID, msg))
            
            #/
            SixyIO.stderr_write_safe(msg, encoding=self.stdee)
            
            #/
            sys.exit(self.exit_code)
        
        #/
        self.ife = ife or SixyIO.IFE
        
        assert self.ife
        
        self.ife_utxt = SixyIO.to_u_safe(self.ife, encoding='ascii')
        
        if not SixyIO.encoding_is_valid(self.ife):
            #/
            msg = SixyIO.format(tt(SixyIO.IFE_NOT_VALID), self.ife_utxt)
            
            #/
            if exit_code is None:
                raisex(AssertionError(SixyIO.IFE_NOT_VALID, msg))
            
            #/
            SixyIO.stderr_write_safe(msg, encoding=self.stdee)
            
            #/
            sys.exit(self.exit_code)
        
        #/
        self.ofe = ofe or SixyIO.OFE
        
        assert self.ofe
        
        self.ofe_utxt = SixyIO.to_u_safe(self.ofe, encoding='ascii')
        
        #/
        if not SixyIO.encoding_is_valid(self.ofe):
            #/
            msg = SixyIO.format(tt(SixyIO.OFE_NOT_VALID), self.ofe_utxt)
            
            #/
            if exit_code is None:
                raisex(AssertionError(SixyIO.OFE_NOT_VALID, msg))
            
            #/
            SixyIO.stderr_write_safe(msg, encoding=self.stdee)
            
            #/
            sys.exit(self.exit_code)
        
        #/
        self.spce = spce or SixyIO.SPCE
        
        assert self.spce
        
        self.spce_utxt = SixyIO.to_u_safe(self.spce, encoding='ascii')
        
        #/
        if not SixyIO.encoding_is_valid(self.spce):
            #/
            msg = SixyIO.format(tt(SixyIO.SPCE_NOT_VALID), self.spce_utxt)
            
            #/
            if exit_code is None:
                raisex(AssertionError(SixyIO.SPCE_NOT_VALID, msg))
            
            #/
            SixyIO.stderr_write_safe(msg, encoding=self.stdee)
            
            #/
            sys.exit(self.exit_code)
        
        #/
        self.spie = spie or SixyIO.SPIE
            
        assert self.spie
        
        self.spie_utxt = SixyIO.to_u_safe(self.spie, encoding='ascii')
        
        #/
        if not SixyIO.encoding_is_valid(self.spie):
            #/
            msg = SixyIO.format(tt(SixyIO.SPIE_NOT_VALID), self.spie_utxt)
            
            #/
            if exit_code is None:
                raisex(AssertionError(SixyIO.SPIE_NOT_VALID, msg))
            
            #/
            SixyIO.stderr_write_safe(msg, encoding=self.stdee)
            
            #/
            sys.exit(self.exit_code)
        
        #/
        self.spoe = spoe or SixyIO.SPOE
        
        assert self.spoe
        
        self.spoe_utxt = SixyIO.to_u_safe(self.spoe, encoding='ascii')
        
        #/
        if not SixyIO.encoding_is_valid(self.spoe):
            #/
            msg = SixyIO.format(tt(SixyIO.SPOE_NOT_VALID), self.spoe_utxt)
            
            #/
            if exit_code is None:
                raisex(AssertionError(SixyIO.SPOE_NOT_VALID, msg))
            
            #/
            SixyIO.stderr_write_safe(msg, encoding=self.stdee)
            
            #/
            sys.exit(self.exit_code)
            
        #/
        self.spee = spee or SixyIO.SPEE
        
        assert self.spee
        
        self.spee_utxt = SixyIO.to_u_safe(self.spee, encoding='ascii')
        
        #/
        if not SixyIO.encoding_is_valid(self.spee):
            #/
            msg = SixyIO.format(tt(SixyIO.SPEE_NOT_VALID), self.spee_utxt)
            
            #/
            if exit_code is None:
                raisex(AssertionError(SixyIO.SPEE_NOT_VALID, msg))
            
            #/
            SixyIO.stderr_write_safe(msg, encoding=self.stdee)
            
            #/
            sys.exit(self.exit_code)
            
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
%-25s%s
%-25s%s""" % (
       u"stdin:", self.stdie_utxt,
       u"stdout:", self.stdoe_utxt,
       u"stderr:", self.stdee_utxt,
       u"cae:", self.cae_utxt,
       u"fse:", self.fse_utxt,
       u"ife:", self.ife_utxt,
       u"ofe:", self.ofe_utxt,
       u"spce:", self.spce_utxt,
       u"spie:", self.spie_utxt,
       u"spoe:", self.spoe_utxt,
       )
    
    def stdin_make_reader(self, encoding=None, errors=None):
        #/
        encoding = encoding or self.stdie
        
        #/
        return SixyIO.stdin_make_reader(encoding=encoding, errors=errors)

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
        
    def spce_to_b(self, txt, encoding=None, errors=None):
        #/
        encoding = encoding or self.spce
        
        #/
        return SixyIO.spce_to_b(txt, encoding=encoding, errors=errors)
        
    def spce_to_b_safe(self, txt, encoding=None, errors=None):
        #/
        encoding = encoding or self.spce
        
        #/
        return SixyIO.spce_to_b_safe(txt, encoding=encoding, errors=errors)
        
    def spie_to_b(self, txt, encoding=None, errors=None):
        #/
        encoding = encoding or self.spie
        
        #/
        return SixyIO.spie_to_b(txt, encoding=encoding, errors=errors)
        
    def spie_to_b_safe(self, txt, encoding=None, errors=None):
        #/
        encoding = encoding or self.spie
        
        #/
        return SixyIO.spie_to_b_safe(txt, encoding=encoding, errors=errors)
        
    def spoe_to_u(self, txt, encoding=None, errors=None):
        #/
        encoding = encoding or self.spoe
        
        #/
        return SixyIO.spoe_to_u(txt, encoding=encoding, errors=errors)
        
    def spoe_to_u_safe(self, txt, encoding=None, errors=None):
        #/
        encoding = encoding or self.spoe
        
        #/
        return SixyIO.spoe_to_u_safe(txt, encoding=encoding, errors=errors)
        
    def spee_to_u(self, txt, encoding=None, errors=None):
        #/
        encoding = encoding or self.spee
        
        #/
        return SixyIO.spee_to_u(txt, encoding=encoding, errors=errors)
        
    def spee_to_u_safe(self, txt, encoding=None, errors=None):
        #/
        encoding = encoding or self.spee
        
        #/
        return SixyIO.spee_to_u_safe(txt, encoding=encoding, errors=errors)
    
    def open_in(self, filename, mode='r', **kwargs):
        #/
        assert SixyIO.is_u(filename)
        
        #/
        return codecs.open(filename, mode, self.ife, **kwargs)
    
    def open_out(self, filename, mode='w', **kwargs):
        #/
        assert SixyIO.is_u(filename)
        
        #/
        file_obj = codecs.open(filename, mode, self.ofe, **kwargs)
        
        #/
        file_obj = FileForceWriteUnicodeWrapper(file_obj, debug_on=self.debug_on)
        
        #/
        return file_obj
