# coding: utf-8

import os

from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',    

    # Точка входа
    (r'^$', 'm3_designer.ide.views.workspace'),
    
    # Файлы проекта
    (r'^project-files$', 'm3_designer.ide.views.get_project_files'), 
                       
    # Создание нового класса в файле    
    (r'^create-new-class$', 'm3_designer.ide.views.create_class'),
    
    # Создание функции инициализации в классе
    (r'^create-autogen-function$', 'm3_designer.ide.views.create_initialize'),
    
    # Создание контейнерной функции 
    (r'^create-function$', 'm3_designer.ide.views.create_cont_func_view'),
                           
    # Возвращает по питоновскому кода, js код
    (r'^designer/upload-code$', 'm3_designer.ide.views.upload_code'),
                       
    # статичный контент проекта
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': settings.MEDIA_ROOT}),
    
    # статичный контент для m3
    (r'^m3static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(settings.M3_ROOT, 'static')}),
    
    (r'^designer$','m3_designer.ide.views.designer'),
    (r'^designer/fake$','m3_designer.ide.views.designer_fake_data'),
    (r'^designer/data$','m3_designer.ide.views.designer_data'),
    (r'^designer/save$','m3_designer.ide.views.designer_save'),
    (r'^designer/preview$','m3_designer.ide.views.designer_preview'),
    (r'^designer/file-content$','m3_designer.ide.views.designer_file_content'),
    (r'^designer/file-content/save$','m3_designer.ide.views.designer_file_content_save'),
    (r'^designer/project-manipulation$','m3_designer.ide.views.designer_structure_manipulation'),
    (r'^designer/project-global-template$','m3_designer.ide.views.designer_global_template_content'),
    (r'^designer/codeassist$','m3_designer.ide.views.codeassist')
)
