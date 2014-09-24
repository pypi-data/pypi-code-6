#coding:utf-8
'''
Регистр накопления (+ остатки)

Created on 12.04.2011

@author: akvarats
'''

from django.db import transaction
from django.db.models import F

from core import PeriodEnum, normdate
from exceptions import GenericRegisterException, WrongRegisterMeta

class CumulativeRegister(object):
    '''
    Базовый управляющий класс для регистров накопления.
    
    При описании прикладного регистра необходимо задавать следующие атрибуты:
    
    * model - модель хранения записей регистра;
    * date_field - наименование поля, которое является системным полем регистра (по умолчанию, date) 
    * period - значение перечисления m3.core.registry.PeriodEnum, которое задает периодичность регистра (по умолчанию, PeriodEnum.DAY);
    * dim_fields - список наименований полей, которые являются измерениями регистра;
    * rest_fields - список наименований полей, которые будут хранить суммарные остатки; 
    * circ_fields - список наименований полей, которые будут хранить суммарные обороты за период;
    '''
    #===========================================================================
    # атрибуты, которые подлежат переопределению в рамках дочерних
    # классов, которые будут управлять конкретными регистрами
    #===========================================================================
    model = None
    submodels = [] # дочерние модели
    
    dim_fields = [] # поля, которые отражают измерения
    rest_fields = [] # поля, которые отражают суммовые поля для остатков 
    circ_fields = [] # поля, которые отражают суммовые поля дл оборотов
    date_field = 'date'
    
    period = PeriodEnum.DAY # по умолчанию считаем, что дефолтный период 
                            # равен одному дню
    
    @classmethod
    @transaction.commit_on_success
    def write(cls, date, **kwargs):
        '''
        Выполняет запись значений в регистр.
        
        Параметры, передаваемые через kwargs должны включать в себя перечисление
        значений по всем измерениям, по которым необходимо произвести сохранить
        остатки и обороты. 
        
        Здесь же, в параметрах, соответствующих наименованиям
        полей хранения остатков (dim_fields) необходимо указывать значение
        изменения остатка в указанном периоде (это может быть положительное,
        либо отрицательное значение).
        '''
        
        cls._check_meta() # проверяем регистр на корректность описания
        
        normalized_date = normdate(cls.period, date)
        
        # формируем единый список обновляемых значений
        allmodels = [cls.model,]
        if cls.submodels:
            allmodels.extend(cls.submodels)
        
        for model in allmodels:
            kw_dims = cls._cleaned_kwargs_by_dims(model, kwargs)
            kw_rests = cls._cleaned_kwargs_by_rests(model, kwargs)
            
            #===================================================================
            # 1. пытаемся понять, если ли запись в регистре на указанную дату
            #===================================================================
            
            # добавляем значение даты в kwargs запроса, поскольку нам нужно
            # понять, существует ли хотя бы одна запись в указанном периоде 
            kw_dims[cls.date_field] = normalized_date
            if not model.objects.filter(**kw_dims).exists():
                # добавляем новую запись регистра с указанной датой
                entry = cls._init_model_instance(model, kwargs)
                setattr(entry, cls.date_field, normalized_date)
                
                # при добавлении новой записи обороты становятся равными нулю,
                # а остатки должны принять наиболее близкое предыдущее значение
                del kw_dims[cls.date_field]
                prev_rests = cls.get(normalized_date, model, **kw_dims)
                kw_dims[cls.date_field] = normalized_date
                
                for i in range(0, len(cls.rest_fields)):
                    setattr(entry, cls.rest_fields[i], prev_rests[i])
                    
                for i in range(0, len(cls.circ_fields)):
                    setattr(entry, cls.circ_fields[i], 0)
                     
                entry.save()
            
            #===================================================================
            # 2. Производим обновление записей об оборотах, если такие параметры
            #    заданы в настройке
            #===================================================================
            if cls.circ_fields:
                update_expr = {}
                
                for i in range(0, len(cls.circ_fields)):
                    update_expr[cls.circ_fields[i]] = F(cls.circ_fields[i]) + kw_rests[cls.rest_fields[i]]
                
                
                model.objects.filter(**kw_dims).update(**update_expr)
            
            #===================================================================
            # 3. Производим update записей регистра (с датами, лежащими после
            #    указанного периода)
            #===================================================================
            
            del kw_dims[cls.date_field]
            kw_dims[cls.date_field + '__gte'] = normalized_date
            update_expr = {}
            
            for field_name in cls.rest_fields:
                    update_expr[field_name] = F(field_name) + kw_rests[field_name]
            
            model.objects.filter(**kw_dims).update(**update_expr)
            
            
    @classmethod
    def get(cls, date, model=None, **kwargs):
        '''
        Возвращает кортеж значений, которые соответствуют записям регистра
        на указанную дату.
        
        В качестве параметра model необходимо передавать либо None (это
        означает использование основной модели хранения, либо
        класс модели, который используется для получения свернутых
        значений.
        
        В возвращаемом кортеже сначала идут значения, которые соответствуют
        полям остаткам, в потом идут значения, соответствующие оборотам.
        '''
        
        result = [0] * (len(cls.rest_fields) + len(cls.circ_fields))
        
        if not model:
            model = cls.model
        else:
            if not model == cls.model and not model in cls.submodels:
                raise GenericRegisterException(u'Указана недопустимый класс подчиненной модели %s при получении данных из регистра %s.' % (model, cls))
        
        normalized_date = normdate(cls.period, date)
        
        kw_dims = cls._cleaned_kwargs_by_dims(model, kwargs)
        kw_dims[cls.date_field + '__lte'] = normalized_date
        
        query = model.objects.filter(**kw_dims).order_by('-' + cls.date_field)[0:1].values_list(*([cls.date_field,] + cls.rest_fields + cls.circ_fields))
        if len(query) > 0:
            for i in range(0, len(cls.rest_fields)):
                result[i] = query[0][i + 1]
                result[len(cls.rest_fields) + i] = query[0][len(cls.rest_fields) + i + 1] if cls._same_dates(normalized_date, query[0][0]) else 0
            
        return tuple(result)
        
        
# ПРИВЕДЕННЫЕ НИЖЕ МЕТОДЫ НЕ ДОПИСАНЫ, ХОТЯ НУЖНЫ В РЕГИСТРАХ
#    @classmethod
#    def get_circs(cls, date_since, date_until, model=None, **kwargs):
#        '''
#        Возвращает значения оборотов по указанным измерениям с начала и
#        по конец указанного периода.
#        
#        Значения в концевых датах включаются в результат
#        '''
#        
#        if not model:
#            model = cls.model
#        else:
#            if not model == cls.model and not model in cls.submodels:
#                raise GenericRegisterException(u'Указана недопустимый класс подчиненной модели %s при получении данных из регистра %s.' % (model, cls))
#        
#        nds = normdate(cls.period, date_since)
#        ndu = normdate(cls.period, date_until)
#        
#        kw_dims = cls._cleaned_kwargs_by_dims(model, kwargs)
#        
#        query = model.objects.filter(**kw_dims).annotate
#        
#    #===========================================================================
#    # Вспомогательные и не интересные функции
#    #===========================================================================
#    @classmethod
#    def drop(cls, date_since=datetime.datetime.min, date_until=datetime.datetime.max, **kwargs):
#        '''
#        Очищает регистр от записей по датам, которые находятся в указанном периоде
#        '''
#        pass 
#        # TODO: вроде бы нужный метод, но пока не работает
#        # формируем единый список обновляемых значений
#        allmodels = [cls.model,]
#        if cls.submodels:
#            allmodels.extend(cls.submodels)
#        
#        for model in allmodels:
#            kw_dims = cls._cleaned_kwargs_by_dims(model, kwargs)
#            # kw_dims.
    
    #===========================================================================
    # Вспомогательные функции
    #===========================================================================
    @classmethod
    def _cleaned_kwargs_by_dims(cls, model, kwargs):
        '''
        Возвращает словарь значений по измерениям на основе указанного kwargs.
        
        В результат включаются только те измерения, которые присутствуют в качестве
        полей указанной модели
        '''
        result = {}
        
        for field in model._meta.fields:
            if (kwargs.has_key(field.name) and 
                field.name in cls.dim_fields):
                result[field.name] = kwargs[field.name]
        
        return result
    
    @classmethod
    def _cleaned_kwargs_by_rests(cls, model, kwargs):
        '''
        Возвращает словарь значений по измерениям на основе указанного kwargs.
        
        В результат включаются только те измерения, которые присутствуют в качестве
        полей указанной модели
        '''
        result = {}
        
        for field in model._meta.fields:
            if (kwargs.has_key(field.name) and 
                field.name in cls.rest_fields):
                result[field.name] = kwargs[field.name]
        
        return result
    
    @classmethod
    def _cleaned_kwargs_by_circs(cls, model, kwargs):
        '''
        Возвращает словарь значений по измерениям на основе указанного kwargs.
        
        В результат включаются только те измерения, которые присутствуют в качестве
        полей указанной модели
        '''
        result = {}
        
        for field in model._meta.fields:
            if (kwargs.has_key(field.name) and 
                field.name in cls.circ_fields):
                result[field.name] = kwargs[field.name]
        
        return result
    
    @classmethod
    def _cleaned_kwargs_by_model(cls, model, kwargs):
        '''
        Преобразует значения, указанные в kwargs в значения 
        '''
        result = {}
        
        for field in model._meta.fields:
            if (kwargs.has_key(field.name)):
                result[field.name] = kwargs[field.name]
        
        return result
    
    @classmethod
    def _init_model_instance(cls, model, kwargs):
        '''
        Инициализирует новую модель 
        '''
        entry = model()
        
        for field in model._meta.fields:
            if kwargs.has_key(field.name):
                setattr(entry, field.name, kwargs[field.name])

        return entry
    
    @classmethod
    def _check_meta(cls):
        '''
        Метод проверяет описание регистра на допустимость
        '''
        if not cls.model:
            raise WrongRegisterMeta(u'Не задана модель хранения записей регистра (%s)' % cls)
        
        
        if not len(cls.rest_fields):
            raise WrongRegisterMeta(u'Не задано ни одно поле регистра для хранения остатков (%s)' % cls)
        
        if len(cls.rest_fields) != len(cls.circ_fields):
            raise WrongRegisterMeta(u'Количество полей для хранения остатков и оборотов регистра должно быть одним и тем же (%s)' % cls)
        
    
    @classmethod
    def _same_dates(cls, date1, date2):
        '''
        Сравнивает два объекта даты/датывремени на равенство.
        '''
        return normdate(cls.period, date1) == normdate(cls.period, date2)
        