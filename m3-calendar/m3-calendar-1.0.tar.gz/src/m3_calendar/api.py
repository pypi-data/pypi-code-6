#coding:utf-8
"""
Created on 31.03.2011

@author: Excinsky
"""
import calendar
from datetime import date, timedelta, datetime
from django.core.exceptions import ObjectDoesNotExist
from m3_calendar.models import ExceptedDayTypeEnum, ExceptedDay


class M3Calendar(object):
    # Сначала я пробовал наследоваться базового питонячьего класса для календаря
    # calendar.Calendar. Но потом передумал, так как не нашел серьезных плюсов.
    """
    Календарь рабочих и выходных дней.

    Позволяет высчитывать рабочие дни по правилам, указанным самим
    пользователем.

    Если появятся дополнительные типы дат, следует дополня
    """
    def __init__(self):
        self.days = set()

        self._db_days_queryset = None
        
        self._work_db_dates = []
        self._off_db_dates = []
        self._holiday_db_dates = []

        self._work_dates = []
        self._off_dates = []
        self._holiday_dates = []

    # TODO(Excinsky): Сейчас, чтобы добавить новый тип дня, надо потрудиться,
    # и объявить специальные свойства для типа дат из БД, типа дат вообще, и
    # функции проверки этих дат, если они не в БД. Это неправильно. Скорее
    # всего тут нужна какая-то абстрактная фабрика. Подумать.

    def get_days_by_period_from_db(self, start_date, end_date,
                                   types=(ExceptedDayTypeEnum.WORKDAY,)):
        """
        Вытаскивает из БД нужные типы дней массивом из питоновских дат.

        Args:
            types: Кортеж из элементов перечисления ExceptedDayTypeEnum.
                Типы дней, которые мы хотим вытащить. По умолчанию вытаскиваем
                рабочие дни.
        """
        self._prepare_db_days(start_date, end_date, types)
        return list(self._db_days_queryset)

    def _work_date_template(self, cdate):
        """
        Функция проверки даты как рабочей среди дат, не перегруженных
        пользователем.
        """
        return cdate.weekday() not in (calendar.SATURDAY, calendar.SUNDAY)

    def _dayoff_date_template(self, cdate):
        """
        Функция проверки даты как выходной среди дат, не перегруженных
        пользователем.
        """
        return cdate.weekday() in (calendar.SATURDAY, calendar.SUNDAY)

    def _holiday_date_template(self, cdate):
        """
        Функция проверки даты как праздничной среди дат, не перегруженных
        пользователем.
        """
        #NOTE(Excinsky): Сюда можно нахлобучить список правздников РФ, например.
        return False

    def _clear_days(self):
        """
        Очищает множество дат, установленных методами работы с периодами.

        Returns: None
        """
        self.days.clear()

    def _clear_db_dates(self):
        self._db_days_queryset = None

        self._work_db_dates = []
        self._off_db_dates = []
        self._holiday_db_dates = []

    def _clear_date_lists(self):
        self._work_dates = []
        self._off_dates = []
        self._holiday_dates = []

    def clear(self):
        self._clear_days()
        self._clear_date_lists()
        self._clear_db_dates()

    # TODO(Excinsky): Аж три фабричных метода подряд. Птички нашептывают, что
    # здесь что-то не так, сынуля.
    def _get_template_function_by_type(self, type):
        """
        Возвращает функцию проверки даты, не перегруженной пользователем.

        Factory method DP.

        Args:
            type: Тип даты. Элемент перечисления ExceptedDayTypeEnum.

        Returns: Функцию проверки даты, не перугруженной пользователем.
        """
        if type == ExceptedDayTypeEnum.WORKDAY:
            return self._work_date_template
        elif type == ExceptedDayTypeEnum.DAYOFF:
            return self._dayoff_date_template
        elif type == ExceptedDayTypeEnum.HOLIDAY:
            return self._holiday_date_template

    def _get_date_list_by_type(self, type):
        """
        Возвращает список дат по типу.

        Factory method DP.

        Args:
            type: Тип даты. Элемент перечисления ExceptedDayTypeEnum.

        Returns: Cписок дат соответствующий указанному типу.
        """
        if type == ExceptedDayTypeEnum.WORKDAY:
            return self._work_dates
        elif type == ExceptedDayTypeEnum.DAYOFF:
            return self._off_dates
        elif type == ExceptedDayTypeEnum.HOLIDAY:
            return self._holiday_dates

    def _get_db_date_list_by_type(self, type):
        """
        Возвращает список дат из БД по типу.

        Factory method DP.

        Args:
            type: Тип даты. Элемент перечисления ExceptedDayTypeEnum.

        Returns: Cписок дат из БД, соответствующий указанному типу.
        """
        if type == ExceptedDayTypeEnum.WORKDAY:
            return self._work_db_dates
        elif type == ExceptedDayTypeEnum.DAYOFF:
            return self._off_db_dates
        elif type == ExceptedDayTypeEnum.HOLIDAY:
            return self._holiday_db_dates

    def _is_day_of_type_db(self, cdate, type):
        """
        Проверка даты среди в списках дат из БД по типу.

        Args:
            cdate: Дата.
            type: Тип даты. Элемент перечисления ExceptedDayTypeEnum.

        Returns: True, если дата нашлась в списке указанного типа.
        """
        if not isinstance(cdate, date):
            raise AttributeError('cdate must be of "date" type')

        if isinstance(cdate, datetime):
            cdate = cdate.date()

        return cdate in self._get_db_date_list_by_type(type)

    def _is_day_of_type_template(self, cdate, type):
        """
        Проверка даты среди дат, не перегруженных пользователем.

        Args:
            cdate: Дата.
            type_: Тип даты. Элемент перечисления ExceptedDayTypeEnum.

        Returns: True, если дата прошла функцию проверки данного типа.
        """
        if not isinstance(cdate, date):
            raise AttributeError('cdate must be of "date" type')

        return self._get_template_function_by_type(type)(cdate)

    def _exclude_days(self, date_list):
        """
        Сокращает множество дней в указанном периоде, хранящемся в self.days.

        Использует разность множеств.

        Args:
            date_list: Список из дат, который необходимо вычесть из текущего
                множества дат.

        Returns: None.
        """
        self.days = self.days.difference(set(date_list))

    def _prepare_days_by_types(self):
        """
        Создает готовые списки дат, раскиданные по типам.

        Returns: None.
        """
        def check_and_exclude_dates(type_, func):
            """
            Проверяет, соответствует ли период дат функции проверки по типу.

            Пробегает по множеству дат в периоде, и, если находит в нем
            даты, соответствующие присланной функции проверки по типу,
            исключает эти даты из общего множества.

            Args:
                type_: Тип даты. Элемент перечисления ExceptedDayTypeEnum.
                func: Функция проверки даты по типу. Должна возвращать булев
                    результат, и принимать в качестве аргументов дату и её тип.

            Returns: None.
            """
            date_list = [day for day in self.days if func(day, type_)]
            self._exclude_days(date_list)
            self._get_date_list_by_type(type_).extend(date_list)

        types = ExceptedDayTypeEnum.values.items()
        for type_, _ in types:
            check_and_exclude_dates(type_, self._is_day_of_type_db)
        for type_, _ in types:
            check_and_exclude_dates(type_, self._is_day_of_type_template)

    def _prepare_db_days(self, start_date, end_date, types):
        """
        Подготавливает списки дат из БД по указанным типам.

        Args:
            start_date: Начальная граница периода. datetime
            end_date: Конечная граница периода. datetime
            types: Типы дней, для которых будет создан специальный QuerySet,
                который потом будет доступен для использования на протяжении
                всей жизни объекта. Список из элементов перечисления
                ExceptedDayTypeEnum.
        """
        def make_queryset(types):
            """
            Создает QuerySet для вытаскивания дат указанных типов из БД.

            Args:
                types: Список из элементов перечисления ExceptedDayTypeEnum.
            """
            return ExceptedDay.objects.filter(day__lte=end_date,
                day__gte=start_date).filter(type__in=types).distinct().order_by(
                'day').values_list('day',flat=True)

        all_db_dates = ExceptedDay.objects.filter(day__lte=end_date,
            day__gte=start_date).filter(
            type__in=ExceptedDayTypeEnum.values.keys())

        self._work_db_dates = [d.day for d in all_db_dates
                               if d.type == ExceptedDayTypeEnum.WORKDAY]
        self._off_db_dates = [d.day for d in all_db_dates
                               if d.type == ExceptedDayTypeEnum.DAYOFF]
        self._holiday_db_dates = [d.day for d in all_db_dates
                               if d.type == ExceptedDayTypeEnum.HOLIDAY]

        self._db_days_queryset = make_queryset(types=types)

    def _prepare_days_for_period_operations(self, start_date, end_date):
        """
        Подготавливает списки с датами всех типов в указанном периоде.

        Args:
            start_date: Начальная граница периода. datetime
            end_date: Конечная граница периода. datetime
        """
        self._clear_days()
        start_end_delta = (end_date - start_date).days

        current_day = start_date
        self.days = set([current_day + timedelta(days=x) for x
                         in xrange(0, start_end_delta)])

        self._prepare_days_by_types()

    def days_by_period(self, start_date, end_date,
                       types=(ExceptedDayTypeEnum.WORKDAY,)):
        """
        Возвращает список дней с указанными типами за данный период.

        Args:
            start_date: Начальная граница периода. datetime
            end_date: Конечная граница периода. datetime
            types: Типы дней, которые надо вытащить. Список из элементов
                перечисления ExceptedDayTypeEnum.

        Returns: Список дат указанных типов, отсортированный по возрастанию.
        """
        self._prepare_db_days(start_date, end_date, types)
        self._prepare_days_for_period_operations(start_date, end_date)

        result_days = []
        for type_ in types:
            result_days.extend(self._get_date_list_by_type(type_))

        result_days.sort()
        self.clear()
        return result_days

    def work_days_by_period(self, start_date, end_date):
        """
        Отдает список всех рабочих дней в периоде.

        Args:
            start_date: Начальная граница периода.
            end_date: Конечная граница периода.

        Returns: Список всех рабочих дат в периоде, отсортированный по
            возрастанию.
        """
        return self.days_by_period(start_date, end_date)

    def weekend_days_by_period(self, start_date, end_date):
        """
        Отдает список всех выходных и праздничных дней в периоде.

        Args:
            start_date: Начальная граница периода.
            end_date: Конечная граница периода.

        Returns: Список всех выходных и праздничных дат в периоде,
            отсортированный по возрастанию.
        """
        return self.days_by_period(start_date, end_date,
               (ExceptedDayTypeEnum.HOLIDAY, ExceptedDayTypeEnum.DAYOFF))

    def work_days_by_bound(self, date, count, bound_since=True):
        """
        Получает отсортированный список рабочих дней в заданном количестве от
        заданной даты в заданном направлении.

        Args:
            date: Дата, являющаяся границей отсчета.
            count: Количество рабочих дней, которое нам нужно получить.
            bound_since: Считаем ли мы date левой границей отрезка? Т.е
                является ли направление просмотра дат "вперед"? Т.е считаем ли
                мы рабочие даты в будущем? True по умолчанию.
        """

        if not count or count < 0:
            raise AttributeError(u'Количество дней должно быть больше нуля')

        def get_supposition_factor(count):
            """
            Коэффициент предполагаемой добавки к количеству всех выбираемых дней,
            в которых находилось достаточно для нас рабочих дней. Посчитан
            примерно как 2/7 + эпсилон в 0,07, отвечающая за праздники.

            Однако, для маленьких чисел множитель лучше ставить побольше,
            чтобы минимизировать количество итераций. Средняя длина итерации
            должна быть где-то ~1.6.

            Выкладки математически не проверены, предполагал интуитивно.

            Args:
                count: Количество рабочих дней, которое нам надо вытащить.
            """
            if count > 14:
                return 0.35
            elif count > 7:
                return 0.7
            elif count > 3:
                return 1
            else:
                return 2

        daycount = int(count * get_supposition_factor(count)) + count
        days = []
        temp_date = date

        while True:
            # Высчитываем рабочие дни из будущего\прошлого.

            # NOTE(Excinsky): Функция days_by_period лезет в БД, поэтому я
            # постарался минимизировать количество итераций. Если будут проблемы
            # с производительностью, надобно хорошенько переписать класс.
            if bound_since:
                new_days = self.days_by_period(temp_date,
                                               temp_date + timedelta(daycount))
            else:
                new_days = self.days_by_period(temp_date - timedelta(daycount),
                                               temp_date)
            # если в текущем рассматриваемом промежутке не нашлось рабочих дней,
            # ищем их в следующем промежутке той же длины
            if not new_days:
                temp_date -= (-1)**bound_since * timedelta(daycount)
                continue
            else:
                days.extend(new_days)
                
            if len(days) < count:
                if bound_since:
                    temp_date = days[-1] + timedelta(1)
                else:
                    days.sort()
                    temp_date = days[0] - timedelta(1)

                temp_count = int(daycount/2)

                daycount = (int(temp_count * get_supposition_factor(temp_count))
                    + temp_count)
                if not daycount:
                    break
            else:
                break

        days.sort()
        if bound_since:
            return days[:count]
        else:
            days.reverse()
            return days[:count]

    @classmethod
    def add_date_to_db(cls, date, type=ExceptedDayTypeEnum.HOLIDAY):
        """
        @static
        Кладет дату в БД с указанным типом.

        Args:
            date: Дата к добавлению.
            type: Элемент перечисления ExceptedDayTypeEnum.
                HOLIDAY по умолчанию.
        """
        try:
            save_date = ExceptedDay.objects.get(day=date)
        except ObjectDoesNotExist:
            save_date = ExceptedDay(day=date)

        save_date.type = type
        save_date.save()