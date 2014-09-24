#coding:utf-8
'''
Модуль содержит описание процессов связей
'''
from datetime import datetime

from django.db import models, transaction

from m3.workflow.core import Workflow, GeneratorWorkflow, WorkflowQueryManager,\
    WorkflowStep, WorkflowOptions
from m3.workflow.meta import MetaWorkflowModel

        
class MetaRelationModel(MetaWorkflowModel):
    ''' Метакласс модели связи. Добавляет поля связи в модель рабочего процесса '''
    def __new__(cls, name, bases, attrs):
        klass = super(MetaRelationModel, cls).__new__(cls, name, bases, attrs)
        # Начало образования связи
        models.DateTimeField(default = datetime.min).contribute_to_class(klass, 'start_date')
        # Конец действия связи
        models.DateTimeField(default = datetime.max).contribute_to_class(klass, 'end_date')
        return klass
    
class GeneratorRelation(GeneratorWorkflow):
    metaclass = 'm3_workflow.MetaRelationModel'
    baseclass = 'm3_workflow.BaseWorkflowModel'
    
class RelationQueryManager(WorkflowQueryManager):
    '''
    Менеджер запросов предоставляющий функции для работы со связями
    '''
    def __init__(self, *args, **kwargs):
        super(RelationQueryManager, self).__init__(*args, **kwargs)
    
    @transaction.commit_on_success
    def create(self, objects = {}, open_docs = {}, date = datetime.min, attr = None):
        '''
        Создает новую открытую связь для объектов objects, открытых документами open_docs на дату date
        @param objects: словарь, где ключи имена полей, а значения экземпляры объектов рабочего набора
        @param open_docs: словарь, где ключи имена полей, а значения экземпляры документов
        @param date: дата с которой включительно начинает действовать связь
        '''
        assert isinstance(objects, dict) and isinstance(open_docs, dict)
        # Создаем новое состояние процесса
        workflow = self.workflow()
        state = self.models.state(step = workflow.state_opened.id)
        state.save()
        
        # Создаем запись связи
        relation = self.models.wf(state = state)
        relation.start_date = date
        relation.attributes = attr
        if hasattr(self.workflow.Meta, 'attributes_model') and not relation.attributes:
            # в случае если в Meta связи объявлена модель атрибутов, а 
            # при создании связи она не передана, то необходимо создать
            # пустую модель для хранения "пустых" значений атрибутов
            relation.attributes = self.workflow.Meta.attributes_model()
        relation.save()
        state.workflow = relation
        state.save()
        
        # Создаем запись рабочего набора
        working_set = self.models.wso(workflow = relation)
        for field_name, obj in objects.items():
            #assert hasattr(working_set, field_name), 'The working set models does not contain a field with the name %s' % field_name
            # В качестве значения могут передаваться как сами записи, так и их id
            if isinstance(obj, int):
                field_name += '_id'
            setattr(working_set, field_name, obj)
        working_set.save()
        
        # FIXME в некоторых случаях не создаются(или не их должно быть) доки. 
        # Вылетает эксепшн. Где ошибка?
        if hasattr(self.workflow.Meta, 'open_docs'):
            # Таблица именованных документов
            open_types = tuple(self.workflow.Meta.open_docs.values())
            named_docs = self.models.nameddocs(workflow = relation)
            for field_name, obj in open_docs.items():
                assert hasattr(named_docs, field_name), 'The named docs models does not contain a field with the name %s' % field_name
                assert isinstance(obj, open_types), 'Document type is not included in the types of opening documents. Look attribute open_docs in Meta.'
                setattr(named_docs, field_name, obj)
            named_docs.save()
        
        #TODO: Пока не знаю нужно ли делать записи в док-модели (модели созданных процессом документов), т.к.
        # они не используются в запросах
        
        workflow.id = relation.id
        workflow.record = relation
        return workflow

    def filter(self, objects, **kwargs):
        '''
        Возвращает запрос к экземплярам связей.
        
        @param objects: Словарь со значениями бизнес-ключей, по которым необходимо наложить разрез
        @param kwargs: Словарь дополнительных свойств операции формирования фильтра
             * opened_only: отбирать только открытые связи
             * closed_only: отбирать только закрытые связи
             * date: дата, на которую отбираются связи
             * start_date: дата начала интервала действия
             * end_date: дата окончания интервала действия связи
        
        Особенности передачи параметров:
        * opened_only имеет приоритет над closed_only. 
        * date имеет приоритет над start_date и end_date. Т.е. заданный параметр date эквивалентен вызову с start_date = date и end_date = date
        
        
        Пример 1. Отобрать все связи, в которые вступил объект obj1:
            MyRelation.objects.filter({'obj_name': obj1})
        
        Пример 2. Отобрать все открытые связи, в которые вступил объект obj1:
            MyRelation.objects.filter({'obj_name': obj1}, opened_only = True)
        
        Пример 3. Отобрать все связи, которые действовали в момент времени date1 для объекта obj1:
            MyRelation.objects.filter({'obj_name': obj1}, date = date1)
        
        Пример 4 (not implemented). Отобрать все связи, которые действовали в момент времени date1 для объекта obj1 и продолжают действовать в текущем состоянии системы:
            MyRelation.objects.filter({'obj_name': obj1}, date = date1, opened_only = True)
        
        Пример 5 (not implemented). Отобрать все связи, которые действовали с момента времени date1:
            MyRelation.objects.filter({'obj_name': obj1}, start_date = date1) 
        
        Пример 6 (not implemented). Отобрать все связи, которые действовали до момента времени date2:
            MyRelation.objects.filter({'obj_name': obj1}, end_date = date2)
            
        Пример 7 (not implemented). Отобрать все связи, которые действовали в интервале времени [date1, date2]
            MyRelation.objects.filter({'obj_name': obj1}, start_date = date1, end_date = date2)
        '''
        
        # считываем параметры запроса
        select_opened = kwargs.pop('opened_only', None)
        select_closed = kwargs.pop('closed_only', None)
        date = kwargs.pop('date', None)
                
        query = self.models.wf.objects
        # фильтр по бизнес-ключам
        for object_name, value in objects:
            if value:
                query = query.filter({'wso__' + object_name: value})
        
        # фильтр по мягким датам
        if date != None:
            query = query.filter({'wf__start_date__lge': date})
            query = query.filter(models.Q({'state__step': 'opened'}) | models.Q({'wf__end_date__gte': date}))
        
        # фильтр по состояниям
        if select_opened != None and select_opened:
            query = query.filter({'state__step': 'opened'})
        elif select_closed != None and select_closed:
            query = query.filter({'state__step': 'closed'})
        
        return query
    
    def filter_old(self, objects, **kwargs):
        '''
        Выполняет запрос к связям по бизнес ключу заданному объектами рабочего набора objects
        В качестве аргументов kwargs могут идти следующие ключи:
          1. opened: bool default True - отбирать только открытые связи
          2. start_soft - мягкое начало периода
          3. start_hard - жесткое начало периода
          4. end_soft - мягкий конец периода
          5. end_hard - жесткий конец период
        Мягкие отличаются от жестких тем, что они включают связи которые частично попадают в период.
        '''
        query = self.models.wso.objects
        # Накладываем фильтр по бизнес-ключу
        for field_name, obj in objects:
            wso_class_name = self.models.wso.__name__.lower()
            filter_key = wso_class_name + '__' + field_name
            query = query.filter({filter_key: obj})
        # Накладываем фильтр по состоянию
        state_class_name = self.models.state.__name__.lower()
        opened = kwargs.pop('opened', True)
        step_id = self.workflow.state_opened.id if opened else self.workflow.state_closed.id
        query = query.filter({state_class_name + '__step': step_id})
        # Накладываем фильтр по периодам действия
        start_date = start_mode = None
        if kwargs.haskey('start_hard'):
            start_date = kwargs.pop('start_hard')
            start_mode = 'hard'
        elif kwargs.haskey('start_soft'):
            start_date = kwargs.pop('start_soft')
            start_mode = 'soft'
        else:
            raise Exception('Start date must be defined!')
        
        end_date = end_mode = None
        if kwargs.haskey('end_hard'):
            end_date = kwargs.pop('end_hard')
            end_mode = 'hard'
        elif kwargs.haskey('end_soft'):
            end_date = kwargs.pop('end_soft')
            end_mode = 'soft'
        else:
            raise Exception('End date must be defined!')
        
        raise NotImplementedError()
    

class RelationOpenedStep(WorkflowStep):
    id = 'opened'
    name = u'Открыто'

class RelationClosedStep(WorkflowStep):
    id = 'closed'
    name = u'Закрыто'

class RelationOptions(WorkflowOptions):
    def __init__(self):
        super(RelationOptions, self).__init__()
        # Пришлось все перенести в процесс. Теперь тут пусто ;)
        attrs = {}
        self.available_attributes.update(attrs)

class Relation(Workflow):
    _objects_class = RelationQueryManager
    _options_class = RelationOptions
    
    def __init__(self):
        super(Relation, self).__init__()
        # Заменяем класс workflow генератора на relation генератор
        self._model_generators.remove(GeneratorWorkflow)
        self._model_generators.insert(0, GeneratorRelation)
        # Состояния
        self.state_opened = RelationOpenedStep()
        self.state_closed = RelationClosedStep()
    
    @transaction.commit_on_success
    def close(self, date, close_docs = {}, resolution = None):
        '''
        Закрывает текущую связь на заданную дату date
        '''
        assert resolution == None or resolution in self.Meta.resolutions, 'Resolution name "%s" not found' % resolution
        # Проверяем не закрыта ли уже текущая связь?
        current_wf = self.models.wf.objects.get(id = self.id)
        current_state = current_wf.state
        if current_state.step == self.state_closed.id:
            raise Exception(u'Relation with id=%s already closed!' % self.id)

        # FIXME в некоторых случаях нет доков. 
        # Вылетает эксепшн. Где ошибка?
        if hasattr(self.Meta, 'close_docs'):
            # Записываем закрывающий документ в связь
            close_types = tuple(self.Meta.close_docs.values())
            named_docs = current_wf.nameddocs
            for field_name, obj in close_docs.items():
                assert hasattr(named_docs, field_name), 'The named docs models does not contain a field with the name %s' % field_name
                assert isinstance(obj, close_types), 'Document type is not included in the types of closed documents. Look attribute close_docs in Meta.'
                setattr(named_docs, field_name, obj)
            named_docs.save()
        
        # Создаем новое состояние
        params = {'step'     : self.state_closed.id,
                  'workflow' : current_wf,
                  'from_step': current_state.step}
        closed_state = self.models.state.objects.create(**params)
        # Указываем наш WF на новый степ
        current_wf.state = closed_state
        current_wf.end_date = date
        current_wf.resolution = resolution
        current_wf.save()
        
    @transaction.commit_on_success
    def delete(self):
        '''
        Физическое удаление записей связи
        '''
        # Каскадное удаление процесса
        current_wf = self.models.wf.objects.get(id = self.id)
        if current_wf.attributes:
            current_wf.attributes.delete()
        current_wf.delete()


