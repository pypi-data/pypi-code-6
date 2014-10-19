# coding: utf-8
"""
File ID: 6qsMRfk
"""

import codecs
import locale
import os
import sys
import yaml

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

class I18n(object):
    #/
    LOAD_LOCALE_TT_FILE_ERR = u'3wLeaR5'
    LOAD_LOCALE_FALLBACK_TT_FILE_ERR = '8cyKaFE'
    
    #/
    TT_DD_K_SYNONYM = 'SYNONYM'
    
    #/
    TT_FILE_EXT_STXT = '.yml'
    TT_FILE_EXT_UTXT = u'.yml'
    
    #/
    FUNC_ARG_DFT = type(None)
    
    #/
    def __init__(self, locale, locale_fallback=None, path_func=None):
        self.tt_dd = {}
        
        self.locale = locale
        
        self.locale_fallback = locale_fallback
        
        self.path_func = path_func
        
        #/
        try:
            self.locale = self.load_tt_file(self.locale)
        except Exception as e:
            raisex(AssertionError(self.LOAD_LOCALE_TT_FILE_ERR, e), None, sys.exc_info()[2])
        
        #/
        if self.locale_fallback and self.locale_fallback != self.locale:
            try:
                self.locale_fallback = self.load_tt_file(self.locale_fallback)
            except Exception as e:
                raisex(AssertionError(self.LOAD_LOCALE_FALLBACK_TT_FILE_ERR, e), None, sys.exc_info()[2])
    
    @staticmethod
    def yaml_force_unicode():
        #/
        ## modified from |http://stackoverflow.com/a/2967461|
        if sys.version_info[0] == 2:
            def construct_func(self, node):
                return self.construct_scalar(node)
            yaml.Loader.add_constructor(u'tag:yaml.org,2002:str', construct_func)
            yaml.SafeLoader.add_constructor(u'tag:yaml.org,2002:str', construct_func)
        
    @staticmethod
    def get_locale_hints(cmdarg=None, fb=None):
        #/
        lang, encoding = locale.getdefaultlocale()
        ## can both be None
        
        #/
        if lang and '_' in lang:
            lang3, _, lang2 = lang.partition('_')
        else:
            lang3 = None
            lang2 = None
        
        #/
        ll_s = [cmdarg, encoding, lang, lang2, lang3, fb]
        ## Encoding comes before lang intentionally, e.g.
        ##  lang |en_US| with encoding |cp936|, |cp936| takes priority.
        
        #/
        ll_s_unique = []
        
        for ll in ll_s:
            if ll:
                ll = ll.lower()
                
                if ll not in ll_s_unique:
                    ll_s_unique.append(ll)
        
        #/
        return ll_s_unique
    
    @staticmethod
    def get_locale_choices(locale_dir):
        #/
        file_name_s = os.listdir(locale_dir)
        
        #/
        choice_s = []
        
        for file_name in file_name_s:
            if file_name.endswith(I18n.TT_FILE_EXT_STXT):
                file_name_noext, _ = os.path.splitext(file_name)
                if file_name_noext:
                    choice_s.append(file_name_noext)
        
        #/
        choice_s = sorted(choice_s)
         
        #/
        return choice_s
    
    def get_locale_file_path(self, locale):
        assert self.path_func
        return self.path_func(locale)
    
    def load_tt_dict(self, tt_d, locale):
        tt_d_old = self.tt_dd.get(locale, None)
        
        if tt_d_old is None:
            self.tt_dd[locale] = tt_d
        else:
            tt_d_old.update(tt_d)
    
    def load_tt_file(self, locale, path=None, encoding=None):
        encoding = encoding or 'utf-8'
        
        if not path:
            assert self.path_func
            path = self.path_func(locale)
            assert path
            
        tt_dd = yaml.load(codecs.open(path, mode='r', encoding=encoding))
        
        synonym = tt_dd.get(self.TT_DD_K_SYNONYM, None)
        
        if synonym:
            return self.load_tt_file(locale=synonym, encoding=encoding)
        
        if locale is None:
            for ll, tt_d in tt_dd.items():
                self.load_tt_dict(tt_d=tt_d, locale=ll)
        else:
            tt_d = tt_dd[locale]
            self.load_tt_dict(tt_d=tt_d, locale=locale)
            
        return locale
    
    def tt(self, key, locale=None, default=FUNC_ARG_DFT):
        #/
        locale = locale or self.locale
        
        #/
        t_dd = self.tt_dd.get(locale, None)
        
        if t_dd is not None:
            #/
            val = t_dd.get(key, self.FUNC_ARG_DFT)
            
            if val is not self.FUNC_ARG_DFT:
                return val
        
        #/
        if self.locale_fallback and self.locale_fallback != locale:
            return self.tt(key, self.locale_fallback, default)
        else:
            if default is I18n.FUNC_ARG_DFT:
                return key
            else:
                return default
            