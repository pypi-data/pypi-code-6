#coding:utf-8
'''
Модуль содержит основные класс и описание моделей рабочих процессов
'''

from django.db import models
from m3.workflow.exceptions import ImproperlyConfigured

#============================================================================
#====================== Шаги рабочего процесса ==============================
#============================================================================
class WorkflowStep(object):
    id = ''
    name = ''
    def __init__(self):
        assert id != '', 'id must be defined!'
    
class WorkflowStartStep(WorkflowStep):
    id = 'new'
    name = u'Новый'
        
class WorkflowEndStep(WorkflowStep):
    id = 'closed'
    name = u'Закрыто'

class Empty:
    pass

#============================================================================
#================== КЛАССЫ ГЕНЕРИРУЮЩИЕ СКРИПТ МОДЕЛЕЙ ======================
#============================================================================

class BaseModelGenerator:
    ''' Базовый класс для генерации скрипта модели '''
    metaclass = ''
    baseclass = ''
    class_suffix = ''
    table_suffix = ''
    attribute = ''
    TEMPLATE = '''
class %(classname)s(%(baseclass)s):
    __metaclass__ = %(metaclass)s
    class Meta:
        db_table = '%(db_table)s'
    class WorkflowMeta:
        workflow = %(class_name)s
    '''
    
    def __init__(self, workflow):
        self.workflow = workflow
    
    def get_class_name(self):
        ''' Функция возвращает название класса модели '''
        return self.workflow.__class__.__name__ + self.class_suffix
    
    def get_table_name(self):
        ''' Функция возвращает название таблицы модели '''
        return self.workflow.meta_dbtable() + self.table_suffix
    
    def get_script(self):
        ''' Возвращает готовый для исполнения скрипт модели '''
        all_params = {'class_name': self.workflow.__class__.__name__,
                      'metaclass' : self.metaclass,
                      'baseclass' : self.baseclass,
                      'classname' : self.get_class_name(),
                      'db_table'  : self.get_table_name()}
        result = self.TEMPLATE % all_params
        return result
    
    def get_register_script(self):
        ''' Регистрирует класс модели в  '''
        if self.attribute:
            # Строка типа: MyWorkflow.models.wf_model = MyWorkflowModel
            script = self.workflow.__class__.__name__ + '.models.' + self.attribute + ' = ' + self.get_class_name()
            script += '\n'
            script += 'assert ' + self.get_class_name() + '!= None \n'
            return script
        return '' 
        
    
class GeneratorWorkflow(BaseModelGenerator):
    metaclass = 'm3_workflow.MetaWorkflowModel'
    baseclass = 'm3_workflow.BaseWorkflowModel'
    class_suffix = 'Model'
    table_suffix = ''
    attribute = 'wf'
    
class GeneratorStep(BaseModelGenerator):
    metaclass = 'm3_workflow.MetaWorkflowStateModel'
    baseclass = 'm3_workflow.BaseWorkflowStepModel'
    class_suffix = 'StateModel'
    table_suffix = 'state'
    attribute = 'state'
    
class GeneratorChild(BaseModelGenerator):
    metaclass = 'm3_workflow.MetaWorkflowChildModel'
    baseclass = 'm3_workflow.BaseWorkflowChildModel'
    class_suffix = 'ChildModel'
    table_suffix = 'child'
    attribute = 'child'
    
class GeneratorWSO(BaseModelGenerator):
    metaclass = 'm3_workflow.MetaWorkflowWSOModel'
    baseclass = 'm3_workflow.BaseWorkflowWSOModel'
    class_suffix = 'WSOModel'
    table_suffix = 'wso'
    attribute = 'wso'
    
class GeneratorDoc(BaseModelGenerator):
    metaclass = 'm3_workflow.MetaWorkflowDocModel'
    baseclass = 'm3_workflow.BaseWorkflowDocModel'
    attribute = 'doc_models'
    def get_class_name(self):
        return self.workflow.meta_dbtable() + 'DocModel'
    
    def get_script(self):
        ''' Отличие в том, что DOC таблиц может быть много и имена будут разные '''
        result = ''
        documents = getattr(self.workflow.Meta, 'documents', [])
        for doc in documents:
            #TODO: Не знаю пока что с этим делать. Пока нет реальных процессов путь отваливается.
            raise NotImplementedError()
            assert isinstance(doc, BaseWorkflowModel)
            result += self.TEMPLATE % \
                     {'class_name': self.__class__.__name__,
                      'db_table':   self.meta_dbtable() + doc.document_class.document_class,
                      'DocModel':   doc.document_class.__name__}
        return result
        
    def get_register_script(self):
        # Тут написать для доков
        script = 'doc_models = {}\n'
        documents = getattr(self.workflow.Meta, 'documents', [])
        for doc in documents: 
            raise NotImplementedError()
            script += 'doc_models["%s"] = %s\n' % ()
        script += self.workflow.__class__.__name__ + '.models.' + self.attribute + ' = doc_models\n'
        return script

class GeneratorNamedDoc(BaseModelGenerator):
    ''' Генератор скрипта для таблицы именованных документов '''
    metaclass = 'm3_workflow.MetaNamedDocsModel'
    baseclass = 'models.Model'
    class_suffix = 'DocModel'
    table_suffix = 'doc'
    attribute = 'nameddocs'

class WorkflowQueryManager(object):
    '''
    Менеджер запросов предоставляющий функции для работы с процессами
    '''
    def __init__(self, workflow):
        self.workflow = workflow
        self.models = workflow.models
    
    def get(self, id):
        '''
        Возвращает экземпляр связи с заданным id
        '''
        wf = self.workflow()
        wf.id = id
        wf.record = self.models.wf.objects.get(id = id)
        return wf
    
    def create(self):
        raise NotImplementedError()
        

#============================================================================
#=================== БАЗОВЫЙ КЛАСС РАБОЧЕГО ПРОЦЕССА ========================
#============================================================================
class WorkflowOptions(object):
    ''' Класс содержащий настройки по умолчанию для рабочих процессов '''
    def __init__(self):
        self.available_attributes = \
        {'db_table': None,  # Имя таблицы процесса
         # Уникальный идентификатор процесса
         'id': None, 
         # Объекты рабочего набора
         'objects': [], 
         # Ссылка на пользовательские атрибуты
         'attributes_model': None,
         # Список причин по которым была закрыта связь
         'resolutions': [],
         # Списоки кортежей состоящих из имени поля и класс документа cпособных открыть новый процесс
         'open_docs': [],   
         # Списоки кортежей состоящих из имени поля и класс документа cпособных открыть новый процесс
         'close_docs': []} 
        
    def create_default_attributes(self):
        for key, value in self.available_attributes.items():
            setattr(self, key, value)
    
    def check_required_attributes(self):
        assert self.id != None, 'Unique process "id" must be defined in Meta class'
        assert self.db_table != None, 'Unique table name "db_table" must be defined in Meta class'
        
    def merge(self, clazz):
        ''' Перезаписывает доступные атрибуты нашего класс значениями сливаемого класса clazz '''
        for key, value in self.available_attributes.items():
            if hasattr(clazz, key):
                value = getattr(clazz, key)
                setattr(self, key, value)
        

class _WorkflowMetaConstructor(type):
    '''
    Метакласс для построения класса рабочего процесса 
    '''
    def __new__(cls, name, bases, attrs):
        klass = super(_WorkflowMetaConstructor, cls).__new__(cls, name, bases, attrs)
        
        # Для каждого экземпляра процесса нужен класс для прямого доспупа к моделям
        klass.models = Empty()
        
        # Инициализации менеджера запросов внутри статического
        # атрибута класса рабочего процесса 
        klass.objects = klass._objects_class(klass)
        
        # Всякий класс сконструированный этим метаклассом будет иметь настройки Meta
        op_class = klass.__dict__.get('_options_class', None)
        if op_class:
            op_ins = op_class()
            op_ins.create_default_attributes()
            meta = getattr(klass, 'Meta', None)
            if meta:
                op_ins.merge(meta)
                #op_ins.check_required_attributes()
            klass.Meta = op_ins

        return klass


class Workflow(object):
    # Определения для хитрого способа создания внутренних менеджеров, специально чтобы их могли переопределить 
    _objects_class = WorkflowQueryManager
    _options_class = WorkflowOptions
    __metaclass__  = _WorkflowMetaConstructor
        
    def __init__(self, *args, **kwargs):
        self.start_step = WorkflowStartStep()
        self.end_step = WorkflowEndStep()
        self.steps = []
        
        # Ключ текущего процесса и запись
        self.id = None
        self.record = None
        
        # Список классов генерирующих код для общего скрипта моделей процесса
        # Так было сделано для возможности перекрыть скрипт каждой отдельной таблицы в потомках
        self._model_generators = [GeneratorWorkflow,
                                  GeneratorStep,
                                  GeneratorChild,
                                  GeneratorWSO,
                                  GeneratorDoc,
                                  GeneratorNamedDoc]
    
    @classmethod
    def meta_class_name(cls):
        '''
        Возвращает имя класса (без префикса модуля)
        '''
        return cls.__name__
    
    @classmethod
    def meta_full_class_name(cls):
        '''
        Возвращает полное квалифицирующее имя класса рабочего потока
        '''
        return cls.__module__ + '.' + cls.__name__
    
    @classmethod    
    def meta_dbtable(cls):
        '''
        Возвращает название таблицы для текущего рабочего потока 
        '''
        try:
            return cls.Meta.db_table
        except:
            raise ImproperlyConfigured('For the class of workflow ' + cls.meta_full_class_name() + ' attribute not set Meta.db_table')
    
    
    @classmethod
    def create_workflow_models(cls):
        ''' Возвращает полный, готовый для выполнения скрипт, генерирующий все модели процесса '''
        model_script = '''
from m3 import workflow as m3_workflow
import %(workflow_module)s
        '''
        model_script = model_script % {'workflow_module': cls.__module__}
        wf = cls()
        
        # Зная имя класса каждой модели можно сразу присвоить их models
        # Получится строка типа: MyWorkflow.models.step = MyWorkflowStateModel
        register_script = '# Assessors \n'
        
        for gen_class in wf._model_generators:
            gen_ins = gen_class(wf)
            model_script += '\n' + gen_ins.get_script()
            register_script += gen_ins.get_register_script() + '\n'
            
        model_script += '\n' # Чтобы в последней строке не было syntax error
        
        return model_script + register_script
    
#============================================================================
#=================== БАЗОВЫЕ КЛАССЫ МОДЕЛЕЙ ПРОЦЕССА ========================
#============================================================================
class BaseWorkflowModel(models.Model):
    ''' Базовый класс для хранимых моделей рабочих потоков '''
    class Meta:
        abstract = True

class BaseWorkflowChildModel(models.Model):
    ''' Базовый класс для хранимых моделей рабочих потоков '''
    class Meta:
        abstract = True

class BaseWorkflowStepModel(models.Model):
    ''' Базовый класс для хранимых моделей шагов рабочих процессов '''
    class Meta:
        abstract = True
        
class BaseWorkflowWSOModel(models.Model):
    class Meta:
        abstract = True

class BaseWorkflowDocModel(models.Model):
    class Meta:
        abstract = True
        
#===============================================================================
# Непонятно что
#===============================================================================

class WorkflowWSObject(object):
    '''
    #TODO: Пока не понятно что это?
    '''
    def __init__(self, wso_class, wso_field):
        '''
        @param wso_class: задает класс модели, которая будет входить в рабочий набор потока
        @param wso_field: задает имя поля, которое используется для храненения идентификатора 
                          соответствующего объекта в моделе WorkflowWSORefModel.
        '''
        self.wso_class = wso_class
        self.wso_field = wso_field

class WorkflowDocument(object):
    '''
    #TODO: Пока не понятно что это?
    '''
    def __init__(self, document_class, document_db_subname):
        self.document_class = document_class
        self.document_db_subname = document_db_subname
    
#===============================================================================
# Переходы рабочего процесса
#===============================================================================
class WorkflowTransition(object):
    def __init__(self, from_step_id, to_step_id, *args, **kwargs):
        self.from_step = None
        self.to_step = None
