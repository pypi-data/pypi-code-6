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
    def raisex(exc, tb=None):
        if tb is not None and exc.__traceback__ is not tb:
            raise exc.with_traceback(tb)
        else:
            raise exc
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

    exec_("""def raisex(exc, tb=None):
    raise exc, None, tb
""")

def reraisex(exc):
    raisex(exc, tb=sys.exc_info()[2])
## ---END

#/
if sys.version_info[0] == 2:
    U = unicode
else:
    U = str

class I18n(object):
    #/
    I18N_CLS_NOT_ALLOW_CREATING_OBJ_ERR = U('9x8Q3un')
    LOAD_LOCALE_TT_FILE_ERR = U('3wLeaR5')
    LOAD_LOCALE_FALLBACK_TT_FILE_ERR = U('8cyKaFE')
    
    #/
    TT_FILE_EXT_STXT = '.yml'
    TT_FILE_EXT_UTXT = U('.yml')
    
    #/
    TT_FILE_K_SYNONYM = 'SYNONYM'
    TT_FILE_K_TT = 'tt'
    
    #/
    DFT = type(None)
    
    def __init__(self):
        """
        Prevent client code from creating object of this class.
        """
        
        msg = U('Can not create object of class I18n. Use class I18nObj instead.')
        
        raisex(AssertionError(I18n.I18N_CLS_NOT_ALLOW_CREATING_OBJ_ERR, msg))
    
    @staticmethod
    def yaml_force_unicode():
        """
        Force pyyaml to return unicode values.
        """
        #/
        ## modified from |http://stackoverflow.com/a/2967461|
        if sys.version_info[0] == 2:
            def construct_func(self, node):
                return self.construct_scalar(node)
            yaml.Loader.add_constructor(U('tag:yaml.org,2002:str'), construct_func)
            yaml.SafeLoader.add_constructor(U('tag:yaml.org,2002:str'), construct_func)
        
    @staticmethod
    def get_locale_hints():
        """
        Get a list of locale hints,
          guessed according to Python's default locale info.
        """
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
        ll_s = [encoding, lang, lang2, lang3]
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
        """
        Get a list of locale file names in the given locale dir.
        """
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
    
class I18nObj(object):
    
    def __init__(self, locale, locale2=None,
        path_func=None,
        file_encoding=None,
        load_file=False,
        ):
        #/
        self.tt_dd = {}
        ## |tt| means text transform.
        ##
        ## |dd| means a dict of dicts.
        ##  The primary dict is indexed by locale keys.
        ##  The secondary dicts are indexed by tt keys.
        
        #/ main locale
        self.locale = locale
        
        #/ fallback locale
        self.locale2 = locale2
        
        #/ locale file path func
        self.path_func = path_func
        
        #/ locale file encoding
        self.file_encoding = file_encoding or 'utf-8'
        
        #/
        if load_file:
            try:
                self.locale = self.load_tt_file(
                    locale=self.locale,
                    path_func=self.path_func,
                    encoding=self.file_encoding,
                )
                ## |load_tt_file| returns the true locale name
                ## in case the original locale file is in synonym format
            except Exception as e:
                reraisex(AssertionError(I18n.LOAD_LOCALE_TT_FILE_ERR, e))
            
            #/
            if self.locale2 and self.locale2 != self.locale:
                try:
                    self.locale2 = self.load_tt_file(
                        locale=self.locale2,
                        path_func=self.path_func,
                        encoding=self.file_encoding,
                    )
                    ## |load_tt_file| returns the true locale name
                    ## in case the original locale file is in synonym format
                except Exception as e:
                    reraisex(AssertionError(I18n.LOAD_LOCALE_FALLBACK_TT_FILE_ERR, e))
    
    def load_tt_dict(self, locale, tt_d):
        """
        Load a tt dict into |self.tt_dd|.
        |tt| means text transform.
        
        locale: key into |self.tt_dd|.
        tt_d: a tt dict.
        """
        
        #/ get the old tt dict of the locale
        tt_d_old = self.tt_dd.get(locale, None)
        
        #/ if has old tt dict
        ## N
        if tt_d_old is None:
            #/ use the new tt dict
            self.tt_dd[locale] = tt_d
        ## Y
        else:
            #/ update the old tt dict
            tt_d_old.update(tt_d)
    
    def load_tt_file(self, locale, path_func=None, encoding=None):
        """
        Load a tt file's tt dict into |self.tt_dd|.
        |tt| means text transform.
        
        locale: locale key into |self.tt_dd|.
        path_func: tt file path func
        encoding: tt file encoding
        """
        
        #/
        path_func = path_func or self.path_func
        
        encoding = encoding or self.file_encoding
        
        #/ get path
        path = path_func(locale)
        
        #/ load dict from locale file
        tt_file_d = yaml.load(codecs.open(path, mode='r', encoding=encoding))
        
        #/
        target_locale = tt_file_d.get(I18n.TT_FILE_K_SYNONYM, None)
        
        #/ if the locale file is in synonym format
        ## Y
        if target_locale:
            #/ load the target locale file instead
            return self.load_tt_file(locale=target_locale, path_func=path_func, encoding=encoding)
        ## N
        
        #/ get the tt dict from the file dict
        tt_d = tt_file_d[I18n.TT_FILE_K_TT]
        
        #/ add to 
        self.load_tt_dict(locale=locale, tt_d=tt_d)
        
        #/ return the true locale
        ## this is useful in case the original locale file is in synonym format
        return locale
    
    def tt(self, key, locale=None, locale2=None, default=I18n.DFT):
        """
        |tt| means text transform.
        
        key: tt key.
        locale: main locale key into |self.tt_dd|. Default to |self.locale|
        locale2: fallback locale key into |self.tt_dd|. Default to |self.locale2|
        default: a default value in case tt value is not found. Default to raise KeyError.
        """
        
        #/
        locale = locale or self.locale
        
        locale2 = locale2 or self.locale2
        
        #/ get tt dict of the locale
        tt_d = self.tt_dd.get(locale, None)
        
        if tt_d is not None:
            #/
            val = tt_d.get(key, I18n.DFT)
            
            #/ if tt value is found
            if val is not I18n.DFT:
                return val
        
        #/ tt value is not found
        
        #/ if has locale2
        ## Y
        if locale2 and locale2 != locale:
            #/ fall back to locale2
            return self.tt(key, locale=locale2, default=default)
        ## N
        else:
            #/ if default is specified
            ## N
            if default is I18n.DFT:
                raise KeyError(key)
            ## Y
            else:
                return default
