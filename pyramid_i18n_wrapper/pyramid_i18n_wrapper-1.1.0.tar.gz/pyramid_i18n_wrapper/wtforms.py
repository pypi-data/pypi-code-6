def wtforms_translation_string_factory(domain):
    '''Let wtforms has lazy translation facility.'''
    
    class _WTFormsLazyTranslationString:
        '''This class used for deferring message translation until rendering stage.'''

        def __init__(self, msg):
            from . import LazyTranslationString
            self.msg = msg
            self.lts = LazyTranslationString(domain)

        def __str__(self):
            return self.lts.translate(self.msg)
    
    return _WTFormsLazyTranslationString


def wtforms_translate_i18n_immediately(form):
    '''
    When using wtforms_translation_string_factory with json renderer,

    '''
    from wtforms import FormField, FieldList
    for key, field in form._fields.items():
        if isinstance(field, FormField):
            wtforms_translate_i18n_immediately(field)
        elif isinstance(field, FieldList):
            for entry in field.entries:
                _translate_field_immediately(entry)
        else:
            _translate_field_immediately(field)

def _translate_field_immediately(field):
    field.label.text = str(field.label.text)
    field.errors = [ str(i) for i in field.errors ]
