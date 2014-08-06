from pexstaticfiles.finders import EggFinder

def serve(request, path, insecure=False, **kwargs):
    '''
    This method mimicks django.contrib.staticfiles.views.serve
    except that it uses pkg_resources to access the static resources 
    (and not using the os module)

    It uses the EggFinder STATICFILES_FINDER regardless of what is set
    in the settings. It makes the same assumption that EGG_STATIC_DIR is
    the name of the static module from which to serve static files.
    '''

    if not settings.DEBUG and not insecure:
        raise ImproperlyConfigured("The staticfiles view can only be used in "
                                   "debug mode or if the --insecure "
                                   "option of 'runserver' is used")
    normalized_path = posixpath.normpath(unquote(path)).lstrip('/')
    resource_path = finders.find(normalized_path)
    if not resource_path:
        if path.endswith('/') or path == '':
            raise Http404("Directory indexes are not allowed here.")
        raise Http404("'%s' could not be found" % path)
    
    

    
