class _ApiObject(object):
    '''
        !!! DON'T USE THIS CLASS DIRECTLY !!!

        Object for add support calls like this:
            vk_obj.audio().search(params)

        method call_api must be redifined in child-class
    '''
    api_section = ''

    def call_api(self, method, params):
        pass

    def __getattr__(self, item):
        if self.api_section:
            return self.api_call_wrapper(item)
        else:
            class _ApiSectionWrapper(object):
                def __init__(self, callback_class):
                    self.callback_class = callback_class
                def __getattr__(self, item):
                    return getattr(self.callback_class, item)
            self.api_section = item
            wrapper = _ApiSectionWrapper(callback_class=self)
            setattr(self, item, wrapper)
            return wrapper

    def api_call_wrapper(self,name):
        def call_func(f_name=name, **kwargs):
            api_func_name = '.'.join([self.api_section, f_name])
            api_params = list(kwargs.items())
            return self.call_api(api_func_name, api_params)
        return call_func
