LANGS_BY_CODE = {} # see hooks.py
LANGS_BY_EID = {} # see hooks.py


def set_lang(lang_eid, lang_dict):
    try:
        old_code = LANGS_BY_EID[lang_eid]['code']
        if lang_dict['code'] != old_code:
            del LANGS_BY_CODE[old_code]
    except KeyError:
        pass # creation case
    LANGS_BY_CODE[lang_dict['code']] = lang_dict
    LANGS_BY_EID[lang_eid] = lang_dict


def remove_lang(lang_eid):
    del LANGS_BY_CODE[LANGS_BY_EID[lang_eid]['code']]
    del LANGS_BY_EID[lang_eid]
