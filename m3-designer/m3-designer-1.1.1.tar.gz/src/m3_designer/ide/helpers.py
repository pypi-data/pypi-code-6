# coding: utf-8

import ast
import os
import codegen
import json

from django.http import HttpResponse

from m3.helpers.icons import Icons

from parser import Parser, ParserError

EXCLUSION = ('pyc', 'orig','ropeproject','hg','hgignore','idea', 'form-backup')
POSIBLE_EDIT_FILES = ('ui.py', 'forms.py')
POSIBLE_EDIT_FILE_PY = 'py'
POSIBLE_FILE_JS = 'js'
POSIBLE_FILE_CSS = 'css'
POSIBLE_FILE_HTML = 'html'
POSIBLE_FILES_IMAGE = ('png', 'jpeg', 'jpg', 'ico', 'gif')

class JsonResponse(HttpResponse):
    def __init__(self, content, *args, **kwargs):        
        kwargs['content_type']='application/json'
        kwargs['content'] = json.dumps(content)      
        super(JsonResponse, self).__init__(*args, **kwargs)
        
def get_files(path, filter_fn = None):
    '''
    Возвращает список всех файлов в проекте
    @param path: Путь до директории с проектом 
    '''    
        
    li = []
 
    for ffile in sorted(os.listdir(path), \
            # Папки имеют приоритет над файлами
            key=lambda x: ' %s' % x if os.path.isdir(os.path.join(path, x)) else x):

        if ffile.split('.')[-1]  in EXCLUSION:
            continue

        if filter_fn is not None and not filter_fn(ffile):
            continue

        # Никаких крокозябр - unicode(..)
        path_file = unicode( os.path.join(path, ffile) )

        propertys_dict = dict(text=ffile)
        propertys_dict['path'] = path_file

        if os.path.isdir(path_file):
            propertys_dict['type'] = 'folder'
            propertys_dict['children'] = get_files(path_file)
            propertys_dict['leaf'] = False

            if '__init__.py' in os.listdir(path_file):
                ''' Признак что папка является packag'ом, изменяет иконку'''
                propertys_dict['iconCls'] = Icons.PACKAGE_PY

        else:
            # Расширение файла (*.py, *.css, ...)
            file_type = ffile.split('.')[-1]
            propertys_dict['type'] = 'file'

            if propertys_dict['text'] in POSIBLE_EDIT_FILES:
                propertys_dict['type'] = 'ui-file'

            #По дефолту является узлом
            propertys_dict['leaf'] = True

            if ffile in POSIBLE_EDIT_FILES:
                propertys_dict['iconCls'] = Icons.PAGE_WHITE_PY
                propertys_dict['leaf'] = False

            elif file_type == POSIBLE_EDIT_FILE_PY:
                propertys_dict['iconCls'] = Icons.PAGE_WHITE_PY

            elif file_type == POSIBLE_FILE_JS:
                propertys_dict['iconCls'] = Icons.PAGE_WHITE_JS

            elif file_type == POSIBLE_FILE_HTML:
                propertys_dict['iconCls'] = Icons.HTML

            elif file_type == POSIBLE_FILE_CSS:
                propertys_dict['iconCls'] = Icons.CSS

            elif file_type in POSIBLE_FILES_IMAGE:
                propertys_dict['iconCls'] = Icons.IMAGE

            else:
                propertys_dict['iconCls'] = Icons.PAGE_WHITE_TEXT
                propertys_dict['attr'] = path_file

        li.append(propertys_dict)

    return li


def get_classess(path):
    '''
    Возвращает набор классов в файле
    '''
    ast_module = ast.parse( Parser.get_source(path) )    
    res = []
    for item in ast_module.body:
        if isinstance(item, ast.ClassDef):
            d = {'text': item.name,
                 #'leaf': True,
                 'iconCls':  'icon-class',
                 'class_name':  item.name,
                 'path': path,
                 'type': 'ui-class'}
            res.append(d)
        
    return res

def get_methods(path, class_name):
    '''
    Возвращает набор методов в классе
    '''
    ast_module = ast.parse( Parser.get_source(path) )    
    res = []
    for item in ast_module.body:
        if isinstance(item, ast.ClassDef) and item.name == class_name:
            for child_item in item.body:
                if isinstance(child_item, ast.FunctionDef):
                    d = {'text': child_item.name,
                         'leaf': True,
                         'iconCls':  'icon-function',
                         'func_name':  child_item.name,
                         'class_name': item.name,
                         'path': path,
                         'type': 'ui-function'}
                    res.append(d)
            break
    return res

def restores(data):
    '''
    Будет пытаться преобразить все символы в кодировку ascii, если это 
    невозможно - если присутсвует unicode символы, то оcтавляет их как есть
    '''
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, dict):
                restores(v)
            elif isinstance(v, list):
                map(restores, v)
            elif isinstance(v, int):
                # Не нужно преобразовывать в юникод
                pass
            else:
                try:
                    data[k] = str(v)
                except UnicodeEncodeError:
                    pass # Итак останется в unicode
    else:
        # Для списков значений
        return data
               
        
def create_py_class(path, class_name, base_class = 'ExtWindow'):
    '''
    Создает класс с функцией автогенерации
    '''
        
    if class_name.find(" ") > 0:
        raise ParserError(u'Наименование класса "%s" не должно содержать пробелов' % class_name)

    if not check_name_syntax(class_name):
        raise ParserError(u'Наименование класса должна начинатся с буквы или "_"')

    try:
        str(class_name)
    except UnicodeEncodeError:
        raise ParserError(u'Наименование класса "%s" должно содержать только ascii символы ' % class_name)
    
    
    source = Parser.get_source(path)

    # Чтение файла        
    module = ast.parse(source)

    #Проверка присутствует ли в модуле класс с именем class_name
    for node in module.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            raise ParserError(u'Наименование класса "%s" уже используется.' % class_name)

    #Нужно добавить импорт всего, если этого импорта нет
    line = 1
    for node in module.body:
        if isinstance(node, ast.ImportFrom):
            line = node.lineno
            if node.module == Parser.IMPORT_ALL:
                break
    else:        
        source_lines = source.split('\n')
        source = '\n'.join(source_lines[:line]) + \
                '\n\n' + codegen.to_source(Parser.generate_import()) + '\n'+ \
                '\n'.join(source_lines[line:])

    f_line = open(path, 'rb').readline()

    # Запись
    with open(path, 'w' if '\r' in f_line else 'wb') as f:
        cl = Parser.generate_class(class_name, base_class)     
        f.write(source + '\n\n\n' +  codegen.to_source(cl))

def generate_func(path, class_name, func_node):
    '''
    Генерирует функции
    @param source: Исходный код функции
    '''
    source = Parser.get_source(path)
    
    module = ast.parse(source)
    
    if not check_name_syntax(func_node.name):
        ParserError(u'Наименование функции должна начинатся с буквы или "_"')

    class_list = filter(lambda x: isinstance(x, ast.ClassDef) and x.name == class_name,
                        module.body)
    for node in class_list and class_list[0].body:
        if node and isinstance(node, ast.FunctionDef) and node.name == func_node.name:
            raise ParserError(u'Наименование функции "%s" уже используется.' % func_node.name)

    for i, node in enumerate(module.body):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            if len(module.body) > i+1:
                line_end = module.body[i+1].lineno
            else:
                line_end = None
            break
    else:
        raise ValueError('Класс "%s" неопределен' % str(class_name) )


    to_source = codegen.to_source(func_node, indentation=1)

    f_line = open(path, 'rb').readline()

    # Запись
    with open(path, 'w' if '\r' in f_line else 'wb') as f:
        if line_end:
            source_lines = source.split('\n')
            f.write('\n'.join(source_lines[:line_end-1]) +
                    '\n' +  to_source + '\n' +
                    '\n'.join(source_lines[line_end-2:]) )
        else:            
            f.write(source + '\n\n' +  to_source)

def create_generation_func(path, class_name):
    '''
    Генерирует функцию для возможности работы с дизайнером форм
    '''
    init_func = Parser.generate_initialize()
    generate_func(path, class_name, init_func)

def create_cont_func(path, class_name, name_func, type_func):
    '''
    Генерирует контейнерную функцию
    '''
    func = Parser.generate_cont_func(name_func, type_func)
    generate_func(path, class_name, func)
    
    

def check_name_syntax(name):
    '''
    Проверяет имя переменной, которое должно начинаться на букву или '_'
    Возвращает True если проверка прошла успешно.
    '''
    if not isinstance(name, basestring):
        raise Exception('Name must be basestring descendant')
    if name[0].isalpha() or name.startswith('_'):
        return True
    return False

def create_structure_node(text='text',children = None, editable = False, path=None):
    '''
    Возвращает словарик представляющий собой вершину структуры
    (исходники проекта, контрибы и тд) для дальнейшей сериализации
    '''
    node = {
                'leaf':False,
                'text':text,
                'type': 'projectRoot' if editable else 'structureNode',
                'iconCls':Icons.FOLDER,
                'children': children
    }

    if path is not None:
        node['path'] = path
    return node