#coding:utf-8

from m3_ext.ui.containers.base import BaseExtContainer
from m3_ext.ui.fields.simple import ExtHiddenField


class ExtAddrComponent(BaseExtContainer):
    '''
    Блок указания адреса
    '''
    PLACE = 1 # Уровнь населенного пункта
    STREET = 2 # Уровнь улицы
    HOUSE = 3 # Уровень дома
    FLAT = 4 # Уровень квартиры

    VIEW_0 = 0 # хитрый режим (пока не будем делать), когда отображается только адрес, а его редактирование отдельным окном
    VIEW_1 = 1 # в одну строку + адрес
    VIEW_2 = 2 # в две строки + адрес, только для level > PLACE
    VIEW_3 = 3 # в три строки + адрес, только для level > STREET

    INVALID_CLASS = 'm3-form-invalid' #Название хтмл-класса м3,
    # который отвечает за стиль отображения неверно заполненных полей
    INVALID_COMPOSITE_FIELD_CLASS = 'm3-composite-field-invalid' #Название класса,
    # отвечающего за прорисовку неверно заполненных композитных полей

    _xtype = 'm3-kladr'

    js_attrs = BaseExtContainer.js_attrs.extend(
        'layout',
        'height',

        invalid_class='params.invalid_class',
        read_only='params.read_only',

        place_label='params.place_label',
        street_label='params.street_label',
        house_label='params.house_label',
        corps_label='params.corps_label',
        flat_label='params.flat_label',
        addr_label='params.addr_label',

        place_field_name='params.place_field_name',
        street_field_name='params.street_field_name',
        house_field_name='params.house_field_name',
        corps_field_name='params.corps_field_name',
        flat_field_name='params.flat_field_name',
        zipcode_field_name='params.zipcode_field_name',
        addr_field_name='params.addr_field_name',

        place_allow_blank='params.place_allow_blank',
        street_allow_blank='params.street_allow_blank',
        house_allow_blank='params.house_allow_blank',
        corps_allow_blank='params.corps_allow_blank',
        flat_allow_blank='params.flat_allow_blank',

        view_mode='params.view_mode',
        level='params.level',
        addr_visible='params.addr_visible',
        use_corps='params.use_corps',
        get_addr_url='params.get_addr_url',
        kladr_url='params.kladr_url',
        street_url='params.street_url',
    )

    deprecated_attrs = BaseExtContainer.deprecated_attrs + (
        'place_field_name',
        'street_field_name',
        'house_field_name',
        'corps_field_name',
        'flat_field_name',
        'zipcode_field_name',
        'addr_field_name',
        'handler_change_place',
        'handler_change_street',
        'handler_change_house',
        'handler_change_flat',
        'handler_change_corps',
        'handler_before_query'
    )

    def __init__(self, *args, **kwargs):
        super(ExtAddrComponent, self).__init__(*args, **kwargs)

        # Названия полей к которым биндится КЛАДР
        self.setdefault('place_field_name', 'place')
        self.setdefault('street_field_name', 'street')
        self.setdefault('house_field_name', 'house')
        self.setdefault('corps_field_name', 'corps')
        self.setdefault('flat_field_name', 'flat')
        self.setdefault('zipcode_field_name', 'zipcode')
        self.setdefault('addr_field_name', 'addr')

        # Названия меток
        self.setdefault('place_label', u'Населенный пункт')
        self.setdefault('street_label', u'Улица')
        self.setdefault('house_label', u'Дом')
        self.setdefault('corps_label', u'Корпус')
        self.setdefault('flat_label', u'Квартира')
        self.setdefault('addr_label', u'Адрес')

        # Атрибуты, определяющие необходимость заполнения полей
        self.setdefault('place_allow_blank', True)
        self.setdefault('street_allow_blank', True)
        self.setdefault('house_allow_blank', True)
        self.setdefault('corps_allow_blank', True)
        self.setdefault('flat_allow_blank', True)

        #Названия инвалидных классов
        self.setdefault('invalid_class', ExtAddrComponent.INVALID_CLASS)
        self.setdefault('invalid_composite_field_class', ExtAddrComponent\
        .INVALID_COMPOSITE_FIELD_CLASS)

        self.setdefault('addr_visible', True)
        self.setdefault('read_only', False)
        self.setdefault('level', ExtAddrComponent.FLAT)
        self.setdefault('view_mode', ExtAddrComponent.VIEW_2)

        # Если True — показывает поле корпуса в режиме >=3
        self.setdefault('use_corps', False)

        self.layout = 'form'
        self.addr = ExtHiddenField(name=self.addr_field_name)
        self.place = ExtHiddenField(name=self.place_field_name)
        self.street = ExtHiddenField(name=self.street_field_name)
        self.house = ExtHiddenField(name=self.house_field_name)
        self.corps = ExtHiddenField(name=self.corps_field_name)
        self.flat = ExtHiddenField(name=self.flat_field_name)
        self.zipcode = ExtHiddenField(name=self.zipcode_field_name)

        self.items.append(self.addr)
        self.items.append(self.place)
        self.items.append(self.street)
        self.items.append(self.house)
        self.items.append(self.corps)
        self.items.append(self.flat)
        self.items.append(self.zipcode)

        # FIXME: Перенести вычисление атрибутов в JS
        # Установка высоты - самый главный хак в этом коде!
        # if self.view_mode == ExtAddrComponent.VIEW_1:
        #     self.height = 25
        # elif self.view_mode == ExtAddrComponent.VIEW_2:
        #     if self.level >= ExtAddrComponent.STREET:
        #         self.height = 25*2
        #     else:
        #         self.height = 25
        # elif self.view_mode == ExtAddrComponent.VIEW_3:
        #     if self.level > ExtAddrComponent.HOUSE:
        #         self.height = 25*3
        #     else:
        #         if self.level > ExtAddrComponent.STREET:
        #             self.height = 25*2
        #         else:
        #             self.height = 25
        # if self.addr_visible:
        #     self.height += 36+7

    # def render_params(self):
    #     def escape_str(in_str):
    #         '''
    #         Экранирует в строке спец. символы, такие как \ ' "
    #         '''

    #         return in_str.replace('"','\"').replace("'","\'").replace('\\', '\\\\')


    #     super(ExtAddrComponent, self).render_params()
    #     self._put_params_value('place_field_name', self.place_field_name)
    #     self._put_params_value('street_field_name', self.street_field_name)
    #     self._put_params_value('house_field_name', self.house_field_name)
    #     self._put_params_value('corps_field_name', self.corps_field_name)
    #     self._put_params_value('flat_field_name', self.flat_field_name)
    #     self._put_params_value('zipcode_field_name', self.zipcode_field_name)
    #     self._put_params_value('addr_field_name', self.addr_field_name)
    #     self._put_params_value('place_label', self.place_label)
    #     self._put_params_value('street_label', self.street_label)
    #     self._put_params_value('house_label', self.house_label)
    #     self._put_params_value('corps_label', self.corps_label)
    #     self._put_params_value('flat_label', self.flat_label)
    #     self._put_params_value('addr_label', self.addr_label)
    #     self._put_params_value('addr_visible', (True if self.addr_visible else False ))
    #     self._put_params_value('level', self.level)
    #     self._put_params_value('view_mode', self.view_mode)
    #     self._put_params_value('read_only', self.read_only)
    #     self._put_params_value('place_value', (self.place.value if self.place and self.place.value else ''))
    #     self._put_params_value('place_record', (self.pack.get_place(self.place.value) if self.place and self.place.value else ''))
    #     #self._put_params_value('place_text', (self.pack.get_place_name(self.place.value) if self.place and self.place.value else ''))
    #     self._put_params_value('place_allow_blank', (True if self.place_allow_blank else False))
    #     self._put_params_value('street_value', (self.street.value if self.street and self.street.value else ''))
    #     #self._put_params_value('street_text', (self.pack.get_street_name(self.street.value) if self.street and self.street.value else ''))
    #     self._put_params_value('street_record', (self.pack.get_street(self.street.value) if self.street and self.street.value else ''))
    #     self._put_params_value('street_allow_blank', (True if self.street_allow_blank else False))
    #     self._put_params_value('house_value', (escape_str(self.house.value) if self.house and self.house.value else ''))
    #     self._put_params_value('house_allow_blank', self.house_allow_blank)
    #     self._put_params_value('corps_value', (escape_str(self.corps.value) if self.corps and self.corps.value else ''))
    #     self._put_params_value('corps_allow_blank', self.corps_allow_blank)
    #     self._put_params_value('flat_value', (escape_str(self.flat.value) if self.flat and self.flat.value else ''))
    #     self._put_params_value('flat_allow_blank', self.flat_allow_blank)
    #     self._put_params_value('zipcode_value', self.get_zipcode())
    #     self._put_params_value('addr_value', (escape_str(self.addr.value) if self.addr and self.addr.value else ''))
    #     self._put_params_value('get_addr_url', (self.pack.get_addr_action.absolute_url() if self.pack.get_addr_action else ''))
    #     self._put_params_value('kladr_url', (self.pack.get_places_action.absolute_url() if self.pack.get_places_action else ''))
    #     self._put_params_value('street_url', (self.pack.get_streets_action.absolute_url() if self.pack.get_streets_action else ''))
    #     self._put_params_value('invalid_class', self.invalid_class)
    #     self._put_params_value('invalid_composite_field_class', self.invalid_composite_field_class)
    #     self._put_params_value('use_corps', self.use_corps)

    # def make_read_only(self, access_off=True, exclude_list=(), *args, **kwargs):
    #     self.read_only = access_off

    # def get_zipcode(self):
    #     '''
    #     получить индекс
    #     на форме есть фиелд zipcode from_object может его заполнить если вдруг индекс мы храним в базе
    #     если он пусто а поле адреса не пустое то возьмемем индекс как первые шесть цифр до пробела
    #     '''
    #     if self.zipcode and self.zipcode.value:
    #         return self.zipcode.value
    #     if self.addr:
    #         addr = self.addr.value
    #         if len(addr)>6:
    #             try:
    #                 return unicode(int(addr[:6]))
    #             except ValueError:
    #                 pass
    #     return ''


    # def render_base_config(self):
    #     res = super(ExtAddrComponent, self).render_base_config()
    #     return res

    # def render(self):
    #     self.render_base_config()
    #     self.render_params()

    #     config = self._get_config_str()
    #     params = self._get_params_str()
    #     return 'new Ext3.m3.AddrField({%s},{%s})' % (config, params)

    # @property
    # def items(self):
    #     return self._items

    # @property
    # def place_field_name(self):
    #     return self._place_field_name

    # @place_field_name.setter
    # def place_field_name(self, value):
    #     self._place_field_name = value
    #     self.place.name = value

    # @property
    # def street_field_name(self):
    #     return self._street_field_name

    # @street_field_name.setter
    # def street_field_name(self, value):
    #     self._street_field_name = value
    #     self.street.name = value

    # @property
    # def house_field_name(self):
    #     return self._house_field_name

    # @house_field_name.setter
    # def house_field_name(self, value):
    #     self._house_field_name = value
    #     self.house.name = value

    # @property
    # def corps_field_name(self):
    #     return self._corps_field_name

    # @corps_field_name.setter
    # def corps_field_name(self, value):
    #     self._corps_field_name = value
    #     self.corps.name = value

    # @property
    # def flat_field_name(self):
    #     return self._flat_field_name

    # @flat_field_name.setter
    # def flat_field_name(self, value):
    #     self._flat_field_name = value
    #     self.flat.name = value

    # @property
    # def zipcode_field_name(self):
    #     return self._zipcode_field_name

    # @zipcode_field_name.setter
    # def zipcode_field_name(self, value):
    #     self._zipcode_field_name = value
    #     self.zipcode.name = value

    # @property
    # def addr_field_name(self):
    #     return self._addr_field_name

    # @addr_field_name.setter
    # def addr_field_name(self, value):
    #     self._addr_field_name = value
    #     self.addr.name = value

    # @property
    # def handler_change_place(self):
    #     return self._listeners.get('change_place')

    # @handler_change_place.setter
    # def handler_change_place(self, function):
    #     self._listeners['change_place'] = function

    # @property
    # def handler_change_street(self):
    #     return self._listeners.get('change_street')

    # @handler_change_street.setter
    # def handler_change_street(self, function):
    #     self._listeners['change_street'] = function

    # @property
    # def handler_change_house(self):
    #     return self._listeners.get('change_house')

    # @handler_change_house.setter
    # def handler_change_house(self, function):
    #     self._listeners['change_house'] = function

    # @property
    # def handler_change_corps(self):
    #     return self._listeners.get('change_corps')

    # @handler_change_corps.setter
    # def handler_change_corps(self, function):
    #     self._listeners['change_corps'] = function

    # @property
    # def handler_change_flat(self):
    #     return self._listeners.get('change_flat')

    # @handler_change_flat.setter
    # def handler_change_flat(self, function):
    #     self._listeners['change_flat'] = function

    # @property
    # def handler_before_query_place(self):
    #     return self._listeners.get('before_query_place')

    # @handler_before_query_place.setter
    # def handler_before_query_place(self, function):
    #     self._listeners['before_query_place'] = function
