#coding:utf-8
'''
Created on 17.06.2011

@author: kirov
'''
from django.conf import settings
from datagrouping import GroupingRecordProvider

try:
    from sqlalchemy import func, desc, and_
except ImportError:
    # sqlalchemy может быть не установлен
    func = desc = and_ = None


class GroupingRecordSQLAlchemyProvider(GroupingRecordProvider):
    '''
    Провайдер для SQLAlchemy
    '''
    def reader(self, grouped, offset, level_index, level_keys, begin, end, aggregates, sorting):
        return self.__read_sqlalchemy(grouped, offset, level_index, level_keys, begin, end, aggregates, sorting)

    def __read_sqlalchemy(self, grouped, offset, level_index, level_keys, begin, end, aggregates, sorting):
        '''
        вывод элементов дерева группировок в зависимости от уровня, ключевых элементов и интервала в уровне
        '''
        # специальный режим, когда считается общий итог по всем записям - не важна сортировка и группировка
        query = self.get_data().subquery()
        if level_index == -1:
            aggr = []
            # будем считать агрегаты
            for agg in aggregates.keys():
                agg_type = aggregates[agg]
                if agg_type == 'sum':
                    aggr.append(func.sum(query.c[agg]).label(agg+'__sum'))
                elif agg_type == 'count':
                    aggr.append(func.count(query.c[agg]).label(agg+'__count'))
                elif agg_type == 'min':
                    aggr.append(func.min(query.c[agg]).label(agg+'__min'))
                elif agg_type == 'max':
                    aggr.append(func.max(query.c[agg]).label(agg+'__max'))
                elif agg_type == 'avg':
                    aggr.append(func.avg(query.c[agg]).label(agg+'__avg'))
            i = self.get_data().session.query(*aggr).select_from(query)[0]
            item = self.create_record()
            item.is_leaf = False
            item.index = None
            item.id = None
            item.indent = None
            item.lindex = None
            for agg in aggregates.keys():
                agg_type = aggregates[agg]
                if agg_type == 'sum':
                    setattr(item, agg, getattr(i,agg + '__sum'))
                elif agg_type == 'count':
                    setattr(item, agg, getattr(i,agg + '__count'))
                elif agg_type == 'min':
                    setattr(item, agg, getattr(i,agg + '__min'))
                elif agg_type == 'max':
                    setattr(item, agg, getattr(i,agg + '__max'))
                elif agg_type == 'avg':
                    setattr(item, agg, getattr(i,agg + '__avg'))
            item.calc()
            return item

        #print 'read_model(): grouped=%s, offset=%s, level_index=%s, level_keys=%s, begin=%s, end=%s' % (grouped, offset, level_index, level_keys, begin, end)
        res = []
        if grouped:
            # для всех группировочных элементов будут использоваться ключи
            # если берется уровень больший, чем количество группировок, то выдаем просто записи
            if level_index >= len(grouped):
                field = None
            else:
                field = grouped[level_index]

            filter = []
            for lev in range(0, level_index):
                lev_field = grouped[lev]
                key = level_keys[lev]
                filter.append(query.c[lev_field] == key)
            aggr = []
            group = []
            if field:
                # будем считать агрегаты
                for agg in aggregates.keys():
                    agg_type = aggregates[agg]
                    if agg_type == 'sum':
                        aggr.append(func.sum(query.c[agg]).label(agg+'__sum'))
                    elif agg_type == 'count':
                        aggr.append(func.count(query.c[agg]).label(agg+'__count'))
                    elif agg_type == 'min':
                        aggr.append(func.min(query.c[agg]).label(agg+'__min'))
                    elif agg_type == 'max':
                        aggr.append(func.max(query.c[agg]).label(agg+'__max'))
                    elif agg_type == 'avg':
                        aggr.append(func.avg(query.c[agg]).label(agg+'__avg'))
                aggr.append(query.c[field])
                aggr.append(func.count(query.c['id']).label('count'))
                group.append(query.c[field])

            if aggr:
                if filter:
                    new_query = self.get_data().session.query(*aggr).select_from(query).filter(and_(*filter)).group_by(*group)
                else:
                    new_query = self.get_data().session.query(*aggr).select_from(query).group_by(*group)
            else:
                if filter:
                    new_query = self.get_data().session.query(query).filter(and_(*filter))
                else:
                    new_query = self.get_data().session.query(query)

            #сортировка
            sort_fields = []
            # TODO: пока сортировка сделана только по одному полю
            if len(sorting.keys()) == 1:
                #необходимо исключить из сортировки поля, которые не входят в aggr, иначе по ним будет сделана ненужная группировка
                if (field and sorting.keys()[0] in aggregates.keys()) or not field:
                    if sorting.values()[0] == 'DESC':
                        sort_fields.append(desc(query.c[sorting.keys()[0]]))
                    else:
                        sort_fields.append(query.c[sorting.keys()[0]])
            if field and not field in sorting:
                #нет заданной сортировки, отсортируем по этому полю
                sort_fields.append(query.c[field])
            if sort_fields:
                new_query = new_query.order_by(*sort_fields)

            # теперь выведем запрошенные элементы уровня
            index = 0
            for i in new_query[begin:end + 1]:
                if field:
                    item = self.create_record()
                    item.is_leaf = False
                    item.index = offset + index + begin
                    item.id = getattr(i,field)
                    item.indent = level_index
                    item.lindex = index + begin
                    item.count = getattr(i,'count')
                    #установим все атрибуты из группировки
                    for lev in range(0, level_index):
                        lev_field = grouped[lev]
                        key = level_keys[lev]
                        setattr(item, lev_field, key)
                    setattr(item, field, getattr(i,field))

                    for agg in aggregates.keys():
                        agg_type = aggregates[agg]
                        if agg_type == 'sum':
                            setattr(item, agg, getattr(i,agg + '__sum'))
                        elif agg_type == 'count':
                            setattr(item, agg, getattr(i,agg + '__count'))
                        elif agg_type == 'min':
                            setattr(item, agg, getattr(i,agg + '__min'))
                        elif agg_type == 'max':
                            setattr(item, agg, getattr(i,agg + '__max'))
                        elif agg_type == 'avg':
                            setattr(item, agg, getattr(i,agg + '__avg'))
                    item.calc()
                else:
                    item = self.create_record()
                    item.is_leaf = True
                    item.index = offset + index + begin
                    item.indent = level_index
                    item.lindex = index + begin
                    item.load(i)
                    item.calc()
                res.append(item)
                index = index + 1
        else:
            # вывести без группировки
            index = 0
            query = self.get_data()
            if len(sorting.keys()) == 1:
                if sorting.values()[0] == 'DESC':
                    query = query.order_by(desc(query.c[sorting.keys()[0]]))
                else:
                    query = query.order_by(query.c[sorting.keys()[0]])
            for i in query[begin:end + 1]:
                item = self.create_record()
                item.indent = 0
                item.is_leaf = True
                item.count = 0
                item.lindex = index + begin
                item.index = index + begin
                item.load(i)
                item.calc()
                res.append(item)
                index = index + 1
        #print 'read_model()= total=%s, res_count=%s' % (total_of_level, len(res))
        #out_cache[cache_key] = (res,total_of_level)
        return res

    def counter(self, grouped, level_index, level_keys, expandedItems):
        return self.__count_sqlalchemy(grouped, level_index, level_keys, expandedItems)

    def __count_sqlalchemy(self, grouped, level_index, level_keys, expandedItems):
        '''
        подсчет количества строк в раскрытом уровне
        '''
        query = self.get_data().subquery()
        #print 'count_model(): grouped=%s, level_index=%s, level_keys=%s, expandedItems=%s' % (grouped, level_index, level_keys, expandedItems)
        total_of_level = 0
        if grouped:
            grouped_ranges = []
            # определим порядок группировки
            for i in grouped:
                grouped_ranges.append(i)

            filter = []
            for lev in range(0, level_index):
                lev_field = grouped_ranges[lev]
                key = level_keys[lev]
                filter.append(query.c[lev_field] == key)
            if level_index < len(grouped_ranges):
                field = grouped_ranges[level_index]
                # т.к. count(distinct не считает поля с null, то будем считать ВЛОБ!
                if filter:
                    total_of_level = self.get_data().session.query(query.c[field]).select_from(query).filter(and_(*filter)).distinct().count()
                else:
                    total_of_level = self.get_data().session.query(query.c[field]).select_from(query).distinct().count()
            else:
                if filter:
                    total_of_level = self.get_data().session.query(query).filter(and_(*filter)).count()
                else:
                    total_of_level = self.get_data().session.query(query).count()

        else:
            total_of_level = self.get_data().count()

        # добавим к количеству также сумму раскрытых элементов
        exp_count = 0
        for exp in expandedItems:
            if exp['count'] == -1:
                exp['count'] = self.counter(grouped, level_index + 1, level_keys + [exp['id']], exp['expandedItems'])
            exp_count = exp_count + exp['count']

        #count_cache[cache_key] = total_of_level+exp_count

        #print 'count_model() = %s, total=%s, exp_count=%s' % (total_of_level + exp_count, total_of_level, exp_count)
        return total_of_level + exp_count

    def indexer(self, grouped, level_index, level_keys, expandedItems, aggregates, sorting):
        return self.__index_sqlalchemy(grouped, level_index, level_keys, expandedItems, aggregates, sorting)

    def __index_sqlalchemy(self, grouped, level_index, level_keys, expandedItems, aggregates, sorting):
        '''
        построение индексов элементов в раскрытом уровне, только для группировок и для тех, которые раскрыты
        '''
        query = self.get_data().subquery()
        res = []
        if grouped and len(expandedItems) > 0:
            # для всех группировочных элементов будут использоваться ключи
            # если берется уровень больший, чем количество группировок, то выдаем просто записи
            field = grouped[level_index]

            filter = []
            for lev in range(0, level_index):
                lev_field = grouped[lev]
                key = level_keys[lev]
                filter.append(query.c[lev_field] == key)
            if filter:
                new_query = self.get_data().session.query(query.c[field]).select_from(query).filter(and_(*filter)).distinct()
            else:
                new_query = self.get_data().session.query(query.c[field]).select_from(query).distinct()
            #сортировка
            sort_fields = []
            if field and not field in sorting:
                #нет заданной сортировки, отсортируем по этому полю
                new_query = new_query.order_by(query.c[field])
            # теперь выведем запрошенные элементы уровня
            for i in new_query:
                res.append(getattr(i,field))
        return res
