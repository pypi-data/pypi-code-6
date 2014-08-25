from natspec_utils.exceptions import MultipleValidationErrors

def multipleMatch(*args):
    import inspect
    methodList = []
    argList = []
    errors = []

    for arg in args:
        if inspect.ismethod(arg):
            methodList.append(arg)
        else:
            argList.append(arg)

    for m in methodList:
        try:
            return m(*argList)
        except (AttributeError, TypeError) as e:
            errors.append(e)

    raise MultipleValidationErrors(errors)