CLASSMETHOD_CALLBACK = "classmethod"

def deckout(callback_type, class_decorator_name):
    def decorator_creator(original_function):
        if callback_type == CLASSMETHOD_CALLBACK:
            def decked_classmethod(self, *args):
                class_wrapper = self.__class__.__dict__[class_decorator_name] 
                new_function = class_wrapper(self, original_function)
                return new_function(self, *args)
            return decked_classmethod 
    return decorator_creator

if __name__ == "__main__":
    class SimpleMathClass(object):
        def wrapper(self, fn):
            def new_fn(self, *args):
                return 3 * fn(self, *args)
            return new_fn

        @deckout("classmethod", "wrapper")
        def my_fn(self, x):
            return x * 2

    b = SimpleMathClass()

    print b.my_fn(5)
