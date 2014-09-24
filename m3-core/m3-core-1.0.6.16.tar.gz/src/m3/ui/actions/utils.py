#coding:utf-8
'''
Вспомогательные функции используемые в паках
'''
from m3.core.exceptions import ApplicationLogicException
import json

from django.db.models.query_utils import Q
from django.db import models


def apply_sort_order(query, columns, sort_order):
    '''
    Закладывает на запрос порядок сортировки. Сначала если в описании колонок columns есть code, 
    то сортируем по нему, иначе если есть по name. Если задан sort_order, то он главнее всех.
    '''
    if isinstance(sort_order, list):
        query = query.order_by(*sort_order)
    else:
        order = None
        for column in columns:
            if isinstance(column, tuple):
                if column[0] == 'name':
                    order = 'name'
                elif column[0] == 'code':
                    order = 'code'
                    break
            elif isinstance(column, dict):
                name = column.get('data_index')
                if name == 'name':
                    order = 'name'
                elif name == 'code':
                    order = 'code'
                    break 
                
        query = query.order_by(order) if order else query.all()
    return query

def create_search_filter(filter_text, fields):
    """
    Фильтрация производится по списку полей fields и введеному пользователем тексту filter_text.
    Возможны два варианта работы.
    1) Если количество слов в запросе <= WORDS_LIMIT, то работаем по следующей схеме
        Пример:
            fields = ['name', 'family']
            filter_text = u'Вася Пупкин'
        Получится условие WHERE:
            (name like 'Вася' AND name like 'Пупкин') OR (family like 'Вася' AND family like 'Пупкин') OR
            ((name like 'Вася' and family like 'Пупкин') OR (name like 'Пупкин' and family like 'Вася'))
    2) Если количество слов в запросе > WORDS_LIMIT, то работаем по следующей схеме
        Пример:
            fields = ['name', 'family']
            filter_text = u'Вася Пупкин Иванович Васильевич Третий'
        Получится условие WHERE:
            ((name like 'Вася Пупкин Иванович Васильевич Третий') OR (family like
                'Вася Пупкин Иванович Васильевич Третий'))
    В случае если нет полей для поиска и выражение Q не сформировалось возвращает None
    """

    # Максимальное количество слов в запросе для работы по сценарию 1(полный перебор)
    WORDS_LIMIT = 3

    def create_filter(words,fields):
        #TODO: нужна оптимизация для исключения повторяющихся условий - сейчас условия повторяются
        filter = None
        if not words or not fields:
            return filter

        if len(words) == 0 or len(fields) == 0:
            return filter

        if len(words) == 1 and len(fields) == 1:
            filter = Q(**{fields.pop() + '__icontains': words.pop()})
            #filter = '('+fields.pop()+'='+words.pop()+')'
            return filter

        if len(words) > 0 and len(fields) == 1:
            field = fields.pop()
            for word in words:
                fltr = Q(**{field + '__icontains': word})
                filter = filter & fltr if filter else fltr
                #fltr = '('+field+'='+word+')'
                #filter = filter+' and '+fltr if filter else fltr
            return filter

        for word in words:
            filtr = None
            for field in fields:
                sub_fltr = create_filter(set(words)-set([word]),set(fields)-set([field]))
                if sub_fltr:
                    fltr = (Q(**{field + '__icontains': word}) & sub_fltr)
                    #fltr = '('+field+'='+word+' and '+sub_fltr+')'
                else:
                    fltr = Q(**{field + '__icontains': word})
                    #fltr = '('+field+'='+word+')'
                filtr = (filtr | fltr) if filtr else fltr
                #filtr = '('+filtr+' or '+fltr+')' if filtr else fltr
            filter = (filter | filtr) if filter else filtr
            #filter = '('+filter+' or '+filtr+')' if filter else filtr
        return filter

    condition = None

    if filter_text:
        words = [filter_text]
        # Если в запросе на поиск <= WORDS_LIMIT слов, то работаем по сценарию 1.
        # Разбиваем текст запроса на слова и осуществляем перебор.
        if len(filter_text.strip().split(' ')) <= WORDS_LIMIT:
            words = filter_text.strip().split(' ')

        condition = None

        # Перебираем все поля.
        for field_name in fields:
            field_condition = None
            # И все слова.
            for word in words:
                q = Q(**{field_name + '__icontains': word})
                field_condition = field_condition & q if field_condition else q

            condition = condition | field_condition if condition else field_condition

        if len(words) <= WORDS_LIMIT:
            # дополнительное условие, если встречаются объединение слов
            cond = create_filter(set(words), set(fields))
            if cond:
                condition = condition | cond if condition else cond

    return condition

def apply_search_filter(query, filter, fields):
    '''
    Накладывает фильтр поиска на запрос. Вхождение каждого элемента фильтра ищется в заданных полях.
    @param query: Запрос
    @param filter: Строка фильтра
    @param fields: Список полей модели по которым будет поиск
    '''
    assert isinstance(fields, (list, tuple))
    condition = create_search_filter(filter, fields)
    if condition != None:
        query = query.filter(condition)
    return query

def detect_related_fields(query, list_columns):
    """
    Определяет необходимость выполнения select_related на запросе.
    """
    # Люди любят указывать в list_columns такие вещи как client.contragent
    # и вообще цеплять вложенные модели. Специально для них генерируем удобный
    # одиночный запрос, который выбирает все что нужно.
    related_models = []
    for column in list_columns:
        if isinstance(column, (tuple, list)):
            column_name = column[0]
        elif isinstance(column, str):
            column_name = column
        elif isinstance(column, dict):
            column_name = column.get('data_index')
            if not column_name:
                continue
        else:
            continue

        if '.' in column_name:
            column_fields = column_name.split('.')
            model_name = column_fields[0]

            # Считаем все что не является последним после точки моделью
            for deep_model in column_fields[1:-1]:
                model_name = model_name +'__'+ deep_model

            related_models.append(model_name)

    new_query = query.select_related(*related_models)
    return new_query

def bind_object_from_request_to_form(request, obj_factory, form, request_id_name = 'id', exclusion=[]):
    '''
    Функция извлекает объект из запроса по id, создает его экземпляр и биндит к форме
    @param request:     Запрос от клиента содержащий id объекта
    @param obj_factory: Функция возвращающая объект по его id
    @param form:        Класс формы к которому привязывается объект
    @param request_id_name:   Имя параметра запроса соответствующего ID объекта
    '''
    # Получаем объект по id
    id = extract_int(request, request_id_name)
    obj = obj_factory(id)
    if obj is None:
        raise ApplicationLogicException('Такого элемента не существует, возможно он был удален.\
                                         Обновите содержимое.')
    # Разница между новым и созданным объектов в том, что у нового нет id или он пустой
    create_new = True
    if isinstance(obj, dict) and obj.get('id') != None:
        create_new = False
    elif hasattr(obj, 'id') and getattr(obj, 'id') != None:
        create_new = False
    # Устанавливаем параметры формы
    win = form(create_new = create_new)
    # Биндим объект к форме
    win.form.from_object(obj, exclusion)
    return win

def bind_request_form_to_object(request, obj_factory, form, request_id_name = 'id', exclusion=[]):
    '''
    Функция создает объект по id в запросе и заполняет его атрибуты из данных пришедшей формы
    @param request:     Запрос от клиента содержащий id объекта
    @param obj_factory: Функция возвращающая объект по его id
    @param form:        Класс формы к которому привязывается объект
    @param request_id_name:   Имя параметра запроса соответствующего ID объекта
    '''
    # Получаем наш объект по id и биндим форму к нему
    id = extract_int(request, request_id_name)
    obj = obj_factory(id)
    
    # Разница между новым и созданным объектов в том, что у нового нет id или он пустой
    create_new = True
    if isinstance(obj, dict) and obj.get('id') != None:
        create_new = False
    elif hasattr(obj, 'id') and getattr(obj, 'id') != None:
        create_new = False

    # Создаем форму для биндинга к ней
    win = form(create_new = create_new)
    win.form.bind_to_request(request)
    win.form.to_object(obj, exclusion)
    
    # Может возникнуть трудноуловимая ошибка, когда в request был id=0 и
    # он присвоился obj.id. В БД не должно быть pk=0
    if not id:
        obj.id = None
    
    return obj

def safe_delete_record(model, id=None):
    '''
    Безопасное удаление записи в базе. В отличие от джанговского ORM не удаляет каскадно.
    Возвращает True в случае успеха, иначе False
    @deprecated нужно использовать BaseModel.safe_delete() или m3.db.safe_delete(obj) 
    '''
    import warnings
    warnings.warn('ui.actions.utils.safe_delete_record(Model, id) must by replaced with m3.db.safe_delete(obj)', DeprecationWarning)
    
    from m3.db import safe_delete
    assert (isinstance(model, models.Model) or issubclass(model, models.Model))
    assert (isinstance(id, int) or isinstance(id, long) or id is None)

    if isinstance(model, models.Model):
        obj = model
    else:
        try:
            obj = model.objects.get(pk=id)
        except model.DoesNotExist:
            #не нашли значит уже удалили
            return True
    return safe_delete(obj)

def fetch_search_tree(model_or_query, filter, branch_id = None, parent_field_name = 'parent'):
    '''
    По заданному фильтру filter и модели model формирует развернутое дерево с результатами поиска.
    Если filter пустой, то получается полностью развернутое дерево.
    '''
    #branch_id - это элемент ограничивающий дерево, т.е. должны возвращаться только дочерние ему элементы
    # Сначала тупо получаем все узлы подходящие по фильтру
    assert isinstance(model_or_query, (models.query.QuerySet, models.Manager)) or issubclass(model_or_query, models.Model)
    if isinstance(model_or_query, (models.query.QuerySet, models.Manager)):
        query = model_or_query
        model = model_or_query.model
    else:
        query = model_or_query.objects
        model = model_or_query
    if branch_id and hasattr(model,'get_descendants'):
        branch_node = query.get(id = branch_id)
        nodes = branch_node.get_descendants().select_related(parent_field_name)
    else:
        nodes = query.all().select_related(parent_field_name)
        
    if filter:
        nodes = nodes.filter(filter)
    
    # Из каждого узла создаем полный путь до корня
    paths = []
    processed_nodes = set()
    for node in nodes:
        # Проверяем не входит ли наш узел в один из просчитанных путей
        if node in processed_nodes:
            continue

        path = [node]
        while getattr(node, parent_field_name):
            if branch_id and getattr(node, parent_field_name) == branch_node:
                break
            if node == getattr(node, parent_field_name):
                break
            node = getattr(node, parent_field_name)
            path.append(node)
            processed_nodes.add(node)
        # Первый элемент пути всегда корень
        path.reverse()
        paths.append(path)

    if len(paths) == 0:
        return []
    
    def create_one_tree(path):
        ''' Превращает путь в дерево с понимаемое ExtJS гридом '''
        tree = path[0]
        for i in range(1, len(path)):
            path[i - 1].children = [path[i]]
        return tree
    
    # Начальное дерево в удобоваримом для грида формате 
    tree = [create_one_tree(paths[0])]
    
    # Слияние путей в одно дерево
    def merge(sub_tree, path_slice):
        try:
            index = sub_tree.index(path_slice[0])
        except ValueError:
            sub_tree.append( create_one_tree(path_slice) )
        else:
            if hasattr(sub_tree[index], 'children'):
                merge(sub_tree[index].children, path_slice[1:])
            else:
                # Значит сливаемый путь оказался длиннее чем высота поддерева
                sub_tree[index].children = [create_one_tree(path_slice[1:])]
                
    for path in paths[1:]:
        merge(tree, path)
    
    def set_tree_attributes(sub_tree):
        '''  Пробегает дерево и устанавливает узлам атрибуты expanded и leaf '''
        if not hasattr(sub_tree, 'children') or len(sub_tree.children) == 0:
            # не факт, что это лист, т.к. мы лишь фильтровали дерево - нужно проверить
            if hasattr(sub_tree,'is_leaf_node'):
                sub_tree.leaf = sub_tree.is_leaf_node()
            else:
                child_nodes = query.filter(Q(**{parent_field_name: sub_tree.id}))
                if len(child_nodes) == 0:
                    sub_tree.leaf = True
        else:
            sub_tree.expanded = True
            for st in sub_tree.children:
                set_tree_attributes(st)
    
    for sub_tree in tree:
        set_tree_attributes(sub_tree)
    
    return tree
    
def extract_int(request, key):
    ''' Извлекает целое число из запроса '''            
    try:
        value = request.REQUEST.get(key, None)
    except IOError:
        # В некоторых браузерах (предполагается что в ie) происходит следующие:
        # request.REQUEST читается и в какой-то момент связь прекращается
        # из-за того, что браузер разрывает соединение, в следствии этого происходит ошибка 
        # IOError: request data read error
        
        #logger.warning(str(err))
        raise
        
    if value:
        # если по каким-то причинам пришло не число, а что-то другое
        try:
            value = int(value)
        except ValueError:
            raise ApplicationLogicException('Произошла ошибка при конвертации.')    
        return value
    else:
        return 0
    
def extract_int_list(request, key):
    ''' Извлекает список целых чисел из запроса '''
    value = request.REQUEST.get(key, '')
    values = map(int, value.split(','))
    return values

def extract_list(request, key):
    data = request.POST.get(key)
    if data:
        obj = json.loads(data)
        if not isinstance(obj, list):
            obj = [obj]
        return obj
    return []

def apply_column_filter(query, request, map):
    '''
    Накладывает колоночный фильтр
    @param query: Запрос
    @param request: Данные с клиента включающие фильтры
    @param map: карта связи фильтров в request и полей в объекте: ключ - поле объекта, значение - параметр фильтра, например:
            {'unit__name':'unit_ref_name'}
    '''
    assert isinstance(map, dict)
    cond = None
    for key, value in map.items():
        filter_word = request.REQUEST.get(value)
        if filter_word:
            filter = Q(**{key+'__icontains': filter_word})
            cond = filter if not cond else (cond & filter)
    if cond:
        query = query.filter(cond)
    return query
