"""
Mods for "django-pdb" :

https://github.com/tomchristie/django-pdb

Generally this Python module is not included in the buildout, you will probably have 
to install it yourself (with "pip")

See the the django-pdb Readme for more usage details.

WARNING: django-pdb should be put at the end of settings.INSTALLED_APPS :
        "Make sure to put django_pdb after any conflicting apps in INSTALLED_APPS so 
        that they have priority."
        
        So with the automatic loading system for the mods, you should enable it with a 
        name like "zpdb", to assure that it is loaded at the end of the loading loop.
"""