#coding: utf-8

from datetime import date, datetime, timedelta
from calendar import calendar

from django.db import models
from django.db.models.query_utils import Q

PERIOD_INFTY = 0 # в регистре нет периодичности и нет динамически хранящихся
PERIOD_SECOND = 1 # до секунд
PERIOD_MINUTE = 2
PERIOD_HOUR = 3
PERIOD_DAY = 4
PERIOD_MONTH = 5
PERIOD_QUARTER = 6
PERIOD_YEAR = 7

def normdate(period, date, begin = True):
    '''
    Метод нормализует дату в зависимости от периода
    @ begin = True - даты выравниваются на начало, иначе на конец
    '''
    if not date:
        return None        
    if period == PERIOD_SECOND:
        return datetime(date.year, date.month, date.day, date.hour, date.minute, date.second)
    if period == PERIOD_MINUTE:
        return datetime(date.year, date.month, date.day, date.hour, date.minute, 0 if begin else 59)
    if period == PERIOD_HOUR:
        return datetime(date.year, date.month, date.day, date.hour, 0 if begin else 59, 0 if begin else 59)
    if period == PERIOD_DAY:
        return datetime(date.year, date.month, date.day, 0 if begin else 23, 0 if begin else 59, 0 if begin else 59)
    if period == PERIOD_MONTH:
        return datetime(date.year, date.month, 1 if begin else calendar.monthrange(date.year, date.month)[1], 0 if begin else 23, 0 if begin else 59, 0 if begin else 59)
    if period == PERIOD_QUARTER:
        if date.month < 4:
            return datetime(date.year, 1 if begin else 3, 1 if begin else calendar.monthrange(date.year, 1 if begin else 3)[1], 0 if begin else 23, 0 if begin else 59, 0 if begin else 59)
        if date.month < 7:
            return datetime(date.year, 4 if begin else 6, 1 if begin else calendar.monthrange(date.year, 4 if begin else 6)[1], 0 if begin else 23, 0 if begin else 59, 0 if begin else 59)
        if date.month < 10:
            return datetime(date.year, 7 if begin else 9, 1 if begin else calendar.monthrange(date.year, 7 if begin else 9)[1], 0 if begin else 23, 0 if begin else 59, 0 if begin else 59)
        return datetime(date.year, 10 if begin else 12, 1 if begin else calendar.monthrange(date.year, 10 if begin else 12)[1], 0 if begin else 23, 0 if begin else 59, 0 if begin else 59)
    if period == PERIOD_YEAR:
        return datetime(date.year, 1 if begin else 12, 1 if begin else calendar.monthrange(date.year, 1 if begin else 12)[1], 0 if begin else 23, 0 if begin else 59, 0 if begin else 59)
    return date

def shift_date(period, date, step = 1):
    '''
    Метод смещает дату на один пункт периода
    @ step = смещение
    '''
    if not date:
        return None        
    elif period == PERIOD_SECOND:
        return date + timedelta(seconds = step)
    elif period == PERIOD_MINUTE:
        return date + timedelta(minutes = step)
    elif period == PERIOD_HOUR:
        return date + timedelta(hours = step)
    elif period == PERIOD_DAY:
        return date + timedelta(days = step)
    elif period == PERIOD_MONTH:
        #TODO: не знаю пока как быстро изменить дату на месяц, т.к. день может быть 31, а в пред. месяце его нет
        return date
    elif period == PERIOD_QUARTER:
        #TODO: не знаю пока как быстро изменить дату
        return date
    elif period == PERIOD_YEAR:
        return datetime(date.year + step, date.month, date.day, date.hour, date.minute, date.second)
    else:
        return date

class OverlapError(Exception):
    """
    Исключение возникающее при наложении интервалов друг на друга.
    """
    def __init__(self, cls=None):
        self.model_cls = cls
#    def __str__(self):
#        return self.exception_message

class InvalidIntervalError(Exception):
    '''
    Исключение возникающее при неверно заданом интервале,
    например если конечная дата меньше начальной.
    '''
    pass

class InfoModelMeta(models.base.ModelBase):
    """
    Магия! Если у модели есть атрибут no_time = True,
    то управляющие поля меняют свой тип с DateTimeField на DateField
    """
    def __new__(cls, name, bases, attrs):
        new_class = super(InfoModelMeta, cls).__new__(cls, name, bases, attrs)
        no_time = attrs.get('no_time', False)
        if no_time:
            # найдем наши базовые классы
            base = None
            for b in bases:
                if issubclass(b, BaseInfoModel) or issubclass(b, BaseIntervalInfoModel):
                    base = b
                    break
            if base:
                for field in list(new_class._meta.local_fields):
                    # найдем наши поля
                    if (issubclass(base, BaseInfoModel) and field.name in ('info_date', 'info_date_prev', 'info_date_next')) or \
                       (issubclass(base, BaseIntervalInfoModel) and field.name in (new_class.begin_src, new_class.end_src, 'info_date_begin', 'info_date_end', 'info_date_prev', 'info_date_next')):
                        # заменим поля на новые
                        if field.default == datetime.min:
                            default = date.min
                        elif field.default == datetime.max:
                            default = date.max
                        else:
                            default = field.default
                        new_field = models.DateField(db_index = field.db_index, default = default)
                        new_class.replace_field(field, new_field)
        # Если в модели определены специальные источники для полей, содержащих дату:
        if hasattr(new_class, 'begin_src') and hasattr(new_class, 'end_src'):

            def _get_fld(name):
                # Возвращает поле из _meta по его name
                return filter(lambda x:x.name == name, list(new_class._meta.local_fields))[0]

            if new_class.begin_src != new_class.DEFAULT_BEGIN:
                # Если в модели переопеределно поле даты начала, info_date_begin нам не нужен. убираем его:
                new_class._meta.local_fields.remove(_get_fld(new_class.DEFAULT_BEGIN))
            if new_class.end_src != new_class.DEFAULT_END:
                # Если в модели переопеределно поле даты конца, info_date_end нам не нужен. убираем его:
                new_class._meta.local_fields.remove(_get_fld(new_class.DEFAULT_END))
        return new_class

    def replace_field(new_class, old_field, new_field):
        """
        Замена полей в классе
        """
        new_class.add_to_class(old_field.name, new_field)
        index = new_class._meta.local_fields.index(old_field)
        new_class._meta.local_fields.remove(old_field)
        new_index = new_class._meta.local_fields.index(new_field)
        new_class._meta.local_fields.insert(index, new_class._meta.local_fields.pop(new_index))

class BaseInfoModel(models.Model):
    __metaclass__ = InfoModelMeta

    # тип управляющих полей по умолчанию остается DateTimeField
    # но может быть изменен на DateField - см. InfoModelMeta
    info_date_prev  = models.DateTimeField(db_index = True, default = datetime.min)
    info_date_next = models.DateTimeField(db_index = True, default = datetime.max)
    info_date = models.DateTimeField(db_index = True, blank = True)
    
    dimentions = [] # перечень реквизитов-измерений
    period = PERIOD_DAY # тип периодичности

    # Константы с минимальной и максимальной датами регистра. Для удобства.
    MAX_DATE = datetime.max
    MIN_DATE = datetime.min

    # сформируем запрос по ключу
    @classmethod
    def query_dimentions(cls, data):
        '''
        запрос по ключевым полям
        @data - объект, который содержит данные для сохранения в регистр.
                Это может быть либо 1) объект модели хранения данных регистра,
                либо 2) словарь, ключами которого являются имена полей из модели хранения,
                либо 3) объект любого класса, у которого есть атрибуты с именами
        '''
        # добавим в запрос фильтр по ключевым полям, со значениями = текущему объекту, переданным данным
        query = cls.objects
        for dim_field in cls.dimentions:
            dim_val = None
            dim_attr = dim_field
            if isinstance(dim_field, models.Field):
                dim_attr = dim_field.name
            if isinstance(data, BaseInfoModel):
                dim_val = getattr(data, dim_attr, None)
            elif isinstance(data, dict):
                if data.has_key(dim_attr):
                    dim_val = data[dim_attr]
            elif hasattr(data, dim_attr):
                dim_val = getattr(data, dim_attr, None)
            if dim_val:
                query = query.filter(**{dim_attr: dim_val})
        return query
    
    # сформируем запрос данных на дату
    @classmethod
    def query_on_date(cls, data, date=None, next = False):
        '''
        запрос записей на дату
        @data - объект или словарь с ключевыми данными
        @date - дата актуальности, по умолчанию текущая
        @next = False - значит будут найдены записи, уже действущие на дату, иначе ближайшиие записи которые будут действовать
        '''
        if date is None:
            date = datetime.now()

        query = cls.query_dimentions(data)
        if cls.period != PERIOD_INFTY:
            q_date = normdate(cls.period,date)
            if next:
                query = query.filter(info_date_prev__lte = q_date, info_date__gt = q_date)
            else:
                if q_date==normdate(cls.period,datetime.max):
                    query = query.filter(info_date__lte = q_date, info_date_next__gte = q_date)
                else:
                    query = query.filter(info_date__lte = q_date, info_date_next__gt = q_date)
        return query
    
    # прямая запись объекта, чтобы можно было записывать без доп. обработки
    def _save(self, *args, **kwargs):
        super(BaseInfoModel, self).save(*args, **kwargs)

    # переопределим запись объекта, чтобы изменять соседние записи
    def save(self, *args, **kwargs):
        # если не указана дата записи, то
        if self.period != PERIOD_INFTY and not self.info_date:
            raise Exception('Attribute info_date is not set!')
        # нормализуем переданные дату и время 
        self.info_date = normdate(self.period,self.info_date)
        
        # проверим на уникальность записи
        if self.period != PERIOD_INFTY:
            q = self.__class__.query_dimentions(self).filter(info_date = self.info_date)
            if self.pk:
                q = q.exclude(pk = self.pk)
            if q.count() > 0:
                raise OverlapError()
        # если объект уже хранится, то найдем записи для изменения
        if self.pk:
            q = self.__class__.query_dimentions(self).filter(info_date = self.info_date_prev).exclude(pk = self.pk)
            old_prev_rec = q.get() if len(q) == 1 else None
            q = self.__class__.query_dimentions(self).filter(info_date = self.info_date_next).exclude(pk = self.pk)
            old_next_rec = q.get() if len(q) == 1 else None
        else:
            old_prev_rec = None
            old_next_rec = None
        # вычислим ближайщую запись, которая начинается "левее" текущей
        q = self.__class__.query_dimentions(self).filter(info_date__lt = self.info_date, info_date_next__gte = self.info_date).exclude(pk = self.pk)
        new_prev_rec = q.get() if len(q) == 1 else None
        # вычислим ближайшую запись, которая начинается "правее" текущей
        q = self.__class__.query_dimentions(self).filter(info_date__gt = self.info_date, info_date_prev__lte = self.info_date).exclude(pk = self.pk)
        new_next_rec = q.get() if len(q) == 1 else None
        # изменим даты исходя из соседей
        if new_prev_rec:
            self.info_date_prev = new_prev_rec.info_date
        else:
            self.info_date_prev = normdate(self.period, self.MIN_DATE)
        if new_next_rec:
            self.info_date_next = new_next_rec.info_date
        else:
            self.info_date_next = normdate(self.period, self.MAX_DATE)
        # сохраним запись
        self._save(*args, **kwargs)
        # изменим найденные ранее записи
        #TODO: тут можно оптимизировать сохранение, чтобы небыло каскада сохранений
        if old_prev_rec:
            if old_prev_rec != new_prev_rec:
                old_prev_rec.save()
        if old_next_rec:
            if old_next_rec != new_next_rec:
                old_next_rec.save()
        if new_prev_rec:
            if new_prev_rec.info_date_next != self.info_date:
                new_prev_rec.info_date_next = self.info_date
                new_prev_rec._save()
        if new_next_rec:
            if new_next_rec.info_date_prev != self.info_date:
                new_next_rec.info_date_prev = self.info_date
                new_next_rec._save()

    # прямое удаление, без обработки
    def _delete(self, *args, **kwargs):
        super(BaseInfoModel, self).delete(*args, **kwargs)

    # переопределим удаление объекта, чтобы изменять соседние записи
    def delete(self, *args, **kwargs):
        # если объект уже хранится, то найдем записи для изменения
        if self.pk:
            q = self.__class__.query_dimentions(self).filter(info_date = self.info_date_prev).exclude(pk = self.pk)
            old_prev_rec = q.get() if len(q) == 1 else None
            q = self.__class__.query_dimentions(self).filter(info_date = self.info_date_next).exclude(pk = self.pk)
            old_next_rec = q.get() if len(q) == 1 else None
        else:
            old_prev_rec = None
            old_next_rec = None
        # удалим запись
        self._delete(*args, **kwargs)
        # изменим найденные ранее записи
        #TODO: тут можно оптимизировать сохранение, чтобы небыло каскада сохранений
        if old_prev_rec:
            old_prev_rec.save()
        if old_next_rec:
            old_next_rec.save()
    
    class Meta:
        abstract = True


def RebuildInfoModel(cls):
    '''
    Перестраивает связи между записями в регистре
    ''' 
    
    def eq_keys(dims, key1, key2):
        for key_attr in dims:
            if key1[key_attr] != key2[key_attr]:
                return False
        return True
    
    def get_key(dims, data):
        key = {}
        for key_attr in dims:
            dim_val = None
            if isinstance(data, BaseInfoModel):
                dim_val = getattr(data, key_attr, None)
            elif isinstance(data, dict):
                if data.has_key(key_attr):
                    dim_val = data[key_attr]
            elif hasattr(data, key_attr):
                dim_val = getattr(data, key_attr, None)
            key[key_attr] = dim_val
        return key
    
    # вытащить записи регистра сгруппированные по ключевым полям и отсортированные по дате
    query = cls.objects
    order = []
    dims = []
    period = cls.period
    for dim_field in cls.dimentions:
        dim_attr = dim_field
        if isinstance(dim_field, models.Field):
            dim_attr = dim_field.name
        order.append(dim_attr)
        dims.append(dim_attr)
    order.append('info_date')
    query.order_by(order)
    # начальное значение ключа = пусто
    last_key = get_key(dims, None)
    last_rec = None
    # бежим по записям
    for rec in query:
        # получим ключ тек. записи
        rec_key = get_key(dims, rec)
        # если тек. ключ не совпадает с предыдущим, то... надо что-то делать
        if not eq_keys(dims, rec_key, last_key):
            # отметим что небыло предыдущих записей
            rec.info_date_prev = normdate(period, datetime.min)
            # если была старая запись, то меняем ее и запишем
            if last_rec:
                last_rec.info_date_next = normdate(period, datetime.max)
                last_rec._save()
        # если ключ совпал, то будем менять связи
        else:
            last_rec.info_date_next = rec.info_date
            last_rec._save()
            rec.info_date_prev = last_rec.info_date
        last_rec = rec
        last_key = rec_key
    # сохраним оставшуюся запись
    if last_rec:
        last_rec.info_date_next = normdate(period, datetime.max)
        last_rec._save()

class BaseIntervalInfoModel(models.Model):
    __metaclass__ = InfoModelMeta
    # Константы по умолчанию для источника даты начала и конца:
    DEFAULT_BEGIN = 'info_date_begin'
    DEFAULT_END = 'info_date_end'

    # тип управляющих полей по умолчанию остается DateTimeField
    # но может быть изменен на DateField - см. InfoModelMeta
    info_date_prev  = models.DateTimeField(db_index = True, default = datetime.min)
    info_date_next = models.DateTimeField(db_index = True, default = datetime.max)
    info_date_begin = models.DateTimeField(db_index = True, blank = True)
    info_date_end = models.DateTimeField(db_index = True, blank = True)
    
    dimentions = [] # перечень реквизитов-измерений
    period = PERIOD_DAY # тип периодичности

    # тут мы можем переопределить,
    # какое поле нам использовать для хранения даты начала.
    # по умолчанию используется info_date_begin
    begin_src = DEFAULT_BEGIN
    # тут мы можем переопределить,
    # какое поле нам использовать для хранения даты конца.
    # по умолчанию используется info_date_end
    end_src = DEFAULT_END
    # Если мы переопередяем какие поля нам использовать,
    # мы сами берем на себя отвественность
    # за настройку полей(тип, индексы, default, allow_blank и т.д.)

    def _get_safe_value(self, fld_name):
        u"""
            Возвращает значение для поля.
            Если значение None,
            то пытается найти значение по умолчанию в мета описании поля.
            Если и в поле не указано значение по умолчанию, то возвращает None
        """
        val = getattr(self, fld_name)
        if val is not None:
            return val
        # Если значение пустое, надо попытаться найти значение по умолчанию:
        fld = filter(lambda x:x.name == fld_name, self._meta.fields)[0]
        return None if fld.default is models.NOT_PROVIDED else fld.default

    @property
    def _begin(self):
        return self._get_safe_value(self.begin_src)
    @_begin.setter
    def _begin(self, val):
        setattr(self, self.begin_src, val)

    @property
    def _end(self):
        return self._get_safe_value(self.end_src)
    @_end.setter
    def _end(self, val):
        setattr(self, self.end_src, val)

    # сформируем запрос по ключу
    @classmethod
    def query_dimentions(cls, data):
        '''
        запрос по ключевым полям
        @data - объект, который содержит данные для сохранения в регистр.
                Это может быть либо 1) объект модели хранения данных регистра,
                либо 2) словарь, ключами которого являются имена полей из модели хранения,
                либо 3) объект любого класса, у которого есть атрибуты с именами
        '''
        # добавим в запрос фильтр по ключевым полям, со значениями = текущему объекту, переданным данным
        query = cls.objects
        for dim_field in cls.dimentions:
            dim_val = None
            dim_attr = dim_field
            if isinstance(dim_field, models.Field):
                dim_attr = dim_field.name
            if isinstance(data, BaseInfoModel):
                dim_val = getattr(data, dim_attr, None)
            elif isinstance(data, dict):
                if data.has_key(dim_attr):
                    dim_val = data[dim_attr]
            elif hasattr(data, dim_attr):
                dim_val = getattr(data, dim_attr, None)
            if dim_val:
                query = query.filter(**{dim_attr: dim_val})
        return query

    @classmethod
    def _gen_Q(cls, src, add, val):
        """
            Возвращает Q выражение
            для динамически состовляемых фильтров по дате начала\конца
                src - указывает дату наачла или конца
                add - постфикс(gte, lte, ...) если просто равенство, то пустая строка
                val значение с которым будем сравнивать
        """
        # шаблон фильтра принимает вид:
        # либо имяполя__постфикс(info_date_end__gte например)
        # или имяполя, если нет постфикса(info_date_end)
        _tmpl = '%s__%s' if add else '%s%s'
        # Возвращаем Q выражение для даты начала
        if src == 'bgn':
            return Q(**{_tmpl % (cls.begin_src, add): val})
        # Возвращаем Q выражение для даты конца
        elif src == 'end':
            return Q(**{_tmpl % (cls.end_src, add): val})
        raise RuntimeError('invalid arg <<src>> for _gen_Q method!')
    
    # сформируем запрос на интервал дат
    @classmethod 
    def query_interval(cls, data, date_begin = datetime.min, date_end = datetime.max, include_begin = True, include_end = True):
        '''
        Выборка записей, попадающий в указанный интервал дат.
        @data - объект или словарь с ключевыми данными
        @date_begin - начало интервала
        @date_end - конец интервала
        @include_begin = True - запись учитывается если начало интервала попадает в интервал записи, иначе не учитывается
        @include_end = True - запись учитывается если конец интервала попадает в интервал записи, иначе не учитывается
        '''
        query = cls.query_dimentions(data)
        if cls.period != PERIOD_INFTY:
            date_begin = normdate(cls.period, date_begin, True)
            date_end = normdate(cls.period, date_end, False)
            filter = cls._gen_Q('bgn', 'gte', date_begin) & cls._gen_Q('end', 'lte', date_end) # попадание в интервал полностью
            if include_begin:
                filter = filter | (cls._gen_Q('bgn', 'lte', date_begin) & cls._gen_Q('end', 'gt', date_begin)) # попадание начала интервала в границы записи
                if include_end:
                    filter = filter | (cls._gen_Q('bgn', 'lt', date_end) & cls._gen_Q('end', 'gte', date_end)) # попадание конца интервала в границы записи
        query = query.filter(filter)
        return query
    
    # сформируем запрос данных на дату
    @classmethod
    def query_on_date(cls, data, date=None, active=True, next=False):
        '''
        запрос записей на дату
        @data - объект или словарь с ключевыми данными
        @date - дата актуальности, по-умолчанию текущая
        @active = True - значит будут найдены записи, действующие на указанную дату
        @next = False - значит будут найдены записи, действовавшие до даты, иначе ближайшиие записи которые будут действовать
        '''
        if date is None:
            date = datetime.now()

        query = cls.query_dimentions(data)
        if cls.period != PERIOD_INFTY:
            q_date_begin = normdate(cls.period, date, True)
            q_date_end = normdate(cls.period, date, False)
            if next:
                filter = Q(info_date_prev__lte = q_date_begin) & cls._gen_Q('bgn', 'gt', q_date_end) # дата попадает в интервал перед записью
            else:
                filter = Q(info_date_next__gt = q_date_end) & cls._gen_Q('end', 'lte', q_date_begin) # дата попадает в интервал после записи
            if active:
                filter = filter | (cls._gen_Q('bgn', 'lte', q_date_begin) & cls._gen_Q('end', 'gte', q_date_end)) # дата попадает в интервал записи
            query = query.filter(filter)
        return query
    
    # прямая запись объекта, чтобы можно было записывать без доп. обработки
    def _save(self, *args, **kwargs):
        super(BaseIntervalInfoModel, self).save(*args, **kwargs)

    # переопределим запись объекта, чтобы изменять соседние записи
    def save(self, *args, **kwargs):
        # если не указана дата записи, то
        if self.period != PERIOD_INFTY and (not self._begin or not self._end):
            raise Exception('Attribute info_date is not set!')
        # нормализуем переданные дату и время 
        self._begin = normdate(self.period,self._begin, True)
        self._end = normdate(self.period,self._end, False)

        if self.period != PERIOD_INFTY and (self._begin > self._end):
            raise InvalidIntervalError("%s > %s"%(self.__class__.begin_src, self.__class__.end_src))
        
        # проверим на уникальность записи
        if self.period != PERIOD_INFTY:
            q = self.__class__.query_interval(self, self._begin, self._end)
            if self.pk:
                q = q.exclude(pk = self.pk)
            if q.count() > 0:
                raise OverlapError( self.__class__ )
        
        # если объект уже хранится, то найдем записи для изменения
        old_prev_rec = None
        old_next_rec = None
        if self.pk:
            q = self.__class__.query_dimentions(self).filter(self.__class__._gen_Q('end','',self.info_date_prev)).exclude(pk = self.pk)
            old_prev_rec = q.get() if len(q) == 1 else None
            q = self.__class__.query_dimentions(self).filter(self.__class__._gen_Q('bgn','',self.info_date_next)).exclude(pk = self.pk)
            old_next_rec = q.get() if len(q) == 1 else None

        # вычислим ближайщую запись, которая заканчивается "левее" текущей
        q = self.__class__.query_dimentions(self).filter(self.__class__._gen_Q('end','lte',self._begin) & Q(info_date_next__gte = self._begin)).exclude(pk = self.pk)
        new_prev_rec = q.get() if len(q) == 1 else None
        # вычислим ближайшую запись, которая начинается "правее" текущей
        q = self.__class__.query_dimentions(self).filter(self.__class__._gen_Q('bgn','gte',self._end) & Q(info_date_prev__lte = self._end)).exclude(pk = self.pk)
        new_next_rec = q.get() if len(q) == 1 else None
        # изменим даты исходя из соседей
        if new_prev_rec:
            self.info_date_prev = new_prev_rec._end
        else:
            self.info_date_prev = normdate(self.period, datetime.min, False)
        if new_next_rec:
            self.info_date_next = new_next_rec._begin
        else:
            self.info_date_next = normdate(self.period, datetime.max, True)
        # сохраним запись
        self._save(*args, **kwargs)
        # изменим найденные ранее записи
        #TODO: тут можно оптимизировать сохранение, чтобы небыло каскада сохранений
        if old_prev_rec:
            if old_prev_rec != new_prev_rec:
                old_prev_rec.save()
        if old_next_rec:
            if old_next_rec != new_next_rec:
                old_next_rec.save()
        if new_prev_rec:
            if new_prev_rec.info_date_next != self._begin:
                new_prev_rec.info_date_next = self._begin
                new_prev_rec._save()
        if new_next_rec:
            if new_next_rec.info_date_prev != self._end:
                new_next_rec.info_date_prev = self._end
                new_next_rec._save()

    # прямое удаление, без обработки
    def _delete(self, *args, **kwargs):
        super(BaseIntervalInfoModel, self).delete(*args, **kwargs)

    # переопределим удаление объекта, чтобы изменять соседние записи
    def delete(self, *args, **kwargs):
        # если объект уже хранится, то найдем записи для изменения
        if self.pk:
            q = self.__class__.query_dimentions(self).filter(self.__class__._gen_Q('end','',self.info_date_prev)).exclude(pk = self.pk)
            old_prev_rec = q.get() if len(q) == 1 else None
            q = self.__class__.query_dimentions(self).filter(self.__class__._gen_Q('bgn', '', self.info_date_next)).exclude(pk = self.pk)
            old_next_rec = q.get() if len(q) == 1 else None
        else:
            old_prev_rec = None
            old_next_rec = None
        # удалим запись
        self._delete(*args, **kwargs)
        # изменим найденные ранее записи
        #TODO: тут можно оптимизировать сохранение, чтобы небыло каскада сохранений
        if old_prev_rec:
            old_prev_rec.save()
        if old_next_rec:
            old_next_rec.save()
    
    class Meta:
        abstract = True


def RebuildIntervalInfoModel(cls, on_overlap_error = 0):
    '''
    Перестраивает связи между записями в интервальном регистре
    on_overlap_error: действие при возникновении ошибки перекрытия диапазонов записей
    0 - вызвать exception
    1 - изменить интервал записи с ранней датой начала
    2 - выдать список ID глючных элементов, которые пропущены (после исправления придется еще раз запускать пересчет)
    ''' 
    
    def eq_keys(dims, key1, key2):
        for key_attr in dims:
            if key1[key_attr] != key2[key_attr]:
                return False
        return True
    
    def get_key(dims, data):
        key = {}
        for key_attr in dims:
            dim_val = None
            if isinstance(data, BaseIntervalInfoModel):
                dim_val = getattr(data, key_attr, None)
            elif isinstance(data, dict):
                if data.has_key(key_attr):
                    dim_val = data[key_attr]
            elif hasattr(data, key_attr):
                dim_val = getattr(data, key_attr, None)
            key[key_attr] = dim_val
        return key
    
    # вытащить записи регистра сгруппированные по ключевым полям и отсортированные по дате
    query = cls.objects
    order = []
    dims = []
    error_ids = []
    period = cls.period
    for dim_field in cls.dimentions:
        dim_attr = dim_field
        if isinstance(dim_field, models.Field):
            dim_attr = dim_field.name
        order.append(dim_attr)
        dims.append(dim_attr)
    order.append(cls.begin_src)
    for field_name in order:
        query = query.order_by(field_name)
    # начальное значение ключа = пусто
    last_key = get_key(dims, None)
    last_rec = None
    # бежим по записям
    for rec in query:
        # получим ключ тек. записи
        rec_key = get_key(dims, rec)
        # если тек. ключ не совпадает с предыдущим, то... надо что-то делать
        if not eq_keys(dims, rec_key, last_key):
            # отметим что небыло предыдущих записей
            rec.info_date_prev = normdate(period, datetime.min, True)
            # если была старая запись, то меняем ее и запишем
            if last_rec:
                last_rec.info_date_next = normdate(period, datetime.max, False)
                last_rec._save()
        # если ключ совпал, то будем менять связи, и проверим перекрытие интервала
        else:
            # попадает ли текущая запись в интервал предыдущей
            if rec._begin < last_rec._end:
                # мы попали...
                # изменим пред. запись
                if on_overlap_error == 1:
                    last_rec._end = normdate(period, shift_date(period, rec._begin, -1), False)
                else:
                    # если ведем лог ошибочных записей, то продолжим
                    if on_overlap_error == 2:
                        error_ids.append(rec.id)
                        continue
                    else:
                        raise OverlapError()
            
            last_rec.info_date_next = rec._begin
            last_rec._save()
            rec.info_date_prev = last_rec._end
        last_rec = rec
        last_key = rec_key
    # сохраним оставшуюся запись
    if last_rec:
        last_rec.info_date_next = normdate(period, datetime.max, False)
        last_rec._save()
    if error_ids and on_overlap_error == 2:
        return error_ids
