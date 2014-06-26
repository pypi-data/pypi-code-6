from distutils.core import setup

desc = """
===
ERP
===

ERP is resource planning system. This is very early version not for using.

Package is being developed in general for modeling and expected to be used
as advanced task management solution at the current stage.

First beta will roll out late july and will contain all to work with
enterprise material and technical base. After beta release work over finance
component would be done.

Detailed documentation would appear in the "docs" directory with beta release.

*********
Changelog
*********
June 26, 2014::
*************************************************************

- All packages moved inside 'erp' package, so now need to import erp.*
- Ajax form support in erp.extras.views is refactored and now works correctly.
- Register view refactored to class-based now and got ajax support now.
======================================
Packages were broken and reuploaded!!!
======================================

June 20, 2014::
*************************************************************

- Added m2m 'res' field to task model with reverse generic relation to 'taskres' model
- Refactored extras.views.AjaxFormMixin to support update form

June 16, 2014::
*************************************************************

- Added 'extras' package, which will contain mixins, fields and abstracts
- Ajax methods develop started with extras.views.AjaxFormMixin
- Done some monkey work with resource serialization

***********
Quick start
***********

1. Add package apps to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'rest_framework',
        'erp.enterprise',
        'erp.planning',
    )

2. Include the polls URLconf in your project urls.py like this::

    url(r'^pm/', include('planning.urls')),
    url(r'^structure/', include('enterprise.urls')),
    url(r'^resource/$', planning.views.ResListView.as_view()),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/reg/$', 'enterprise.views.register'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

3. Add custom auth app to your project settings.py like this:

    AUTH_USER_MODEL = 'erp.enterprise.CorpUser'

4. Run `python manage.py syncdb` to create models.

5. Copy templates and static files from package file to your project's dir.

6. Visit http://127.0.0.1:8000/ to get started.

7. Forgive me ^_^
"""

setup(
    name='ERP',
    version='0.17',
    packages=['erp', 'erp.extras', 'erp.planning', 'erp.enterprise'],
    url='https://github.com/CLTanuki/RPS',
    license='BSD License',
    author='CLTanuki',
    author_email='CLTanuki@gmail.com',
    description='Resourse Planning System',
    long_description=desc,
    install_requires=[
        'django',
        'djangorestframework',
    ],
    include_package_data=True,
    # package_data={
    #     'enterprise': ['templates/*.html',
    #                    'templates/registration/*'],
    #     'planning': ['templates/*.html',
    #                  'templates/planning/*'],
    #
    # },
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Development Status :: 2 - Pre-Alpha',
    ],
)
