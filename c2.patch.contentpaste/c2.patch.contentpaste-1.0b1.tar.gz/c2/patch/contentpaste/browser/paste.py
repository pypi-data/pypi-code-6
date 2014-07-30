# coding: utf-8
from random import random
from DateTime import DateTime
import transaction
from Acquisition import aq_inner, aq_parent
from AccessControl import Unauthorized
from ZODB.POSException import ConflictError
from zope.i18n import translate
from zope.interface import providedBy
from zope.component import getUtility
from Products.Five import BrowserView
from Products.ATContentTypes.interfaces.interfaces import IATContentType
from Products.Archetypes.interfaces.field import IFileField
from Products.Archetypes.interfaces.field import ITextField
from plone.app.blob.interfaces import IBlobField
from plone.i18n.normalizer.interfaces import IIDNormalizer
from zope.container.interfaces import INameChooser
try:
     from plone.dexterity.interfaces import IDexterityContent
     from plone.dexterity.utils import getAdditionalSchemata
     from zope.schema import getFieldsInOrder
     DEXTERITY_INSTALLED = True
except ImportError:
     DEXTERITY_INSTALLED = False

from c2.patch.contentpaste import ContentPasteMessageFactory as _

from logging import getLogger
logger = getLogger(__name__)
info = logger.info

# COPY_TARGET_SCHEMATAS = ['default',]
COPY_IGNORE_SCHEMATAS = ['dates', 'ownership', 'settings']
COPY_IGNORE_FIELDS = set(('id', 'effective', 'expires', 'creators'))
ADDING_TITLE = _(u"copy_of_")

def _get_schemata_fields(obj, schemata):
    return obj.schema.getSchemataFields(schemata)

def _get_ignore_fields_in_schematas(obj):
    for schemata in COPY_IGNORE_SCHEMATAS:
        for field in _get_schemata_fields(obj, schemata):
            yield field.getName()

def _get_all_at_field(obj):
    return obj.Schema().keys()

def _copy_at_fields(obj):
    all_field_set = set(_get_all_at_field(obj))
    ignore_field_set = set(_get_ignore_fields_in_schematas(obj)) | \
                            COPY_IGNORE_FIELDS
    copy_fields = all_field_set - ignore_field_set
    for field_name in copy_fields:
        dic = {'field_name' : field_name}
        field = obj.getField(field_name)
        if ITextField in providedBy(field):
            dic['contenttype'] = field.getContentType(obj)
            dic['data'] = field.getRaw(obj)
        elif IFileField in providedBy(field):
            field_data = field.getRaw(obj)
            if field_data:
                dic['filename'] = field.getFilename(obj)
                dic['data'] = field_data.data
        elif IBlobField in providedBy(field):
            field_data = field.getRaw(obj)
            if field_data:
                dic['filename'] = field_data.getFilename()
                dic['data'] = field_data.data
                dic['is_blob'] = True
        else:
            dic['data'] = field.getRaw(obj)
        yield dic

def _get_all_dx_field(obj):
    for name, field in getFieldsInOrder(obj.getTypeInfo().lookupSchema()):
        yield name, field
    additional_schemata = getAdditionalSchemata(obj)
    for additional in additional_schemata:
        for name, field in getFieldsInOrder(additional):
            yield name, field

def _copy_dx_fields(obj):
    all_field_dic = dict(_get_all_dx_field(obj))
    for ignore_field in COPY_IGNORE_FIELDS:
        if ignore_field in all_field_dic:
            del all_field_dic[ignore_field]
    for field_name, field in all_field_dic.items():
        dic = {'field_name' : field_name}
        try:
            dic['data'] = getattr(getattr(obj, field_name), 'output', getattr(obj, field_name))
        except:
            info("Could NOT get field name: %s" %(field_name))
        yield dic

def _generate_unique_id(type_name=None):
    now = DateTime()
    time = '%s.%s' % (now.strftime('%Y-%m-%d'), str(now.millis())[7:])
    rand = str(random())[2:6]
    prefix = ''
    suffix = ''
    if type_name is not None:
        prefix = type_name.replace(' ', '_')+'.'
    prefix = prefix.lower()
    return prefix + time + rand + suffix

def set_field_at_types(obj, new_obj, request):
    for field_dic in _copy_at_fields(obj):
        field_name = field_dic['field_name']
        data  = field_dic.get('data', '')
        filename = field_dic.get('filename', None)
        contenttype = field_dic.get('contenttype', None)
        if field_name == 'title':
            adding_data = translate(ADDING_TITLE, context=request)
            if isinstance(data, unicode):
                data_save = adding_data + data
            else:
                data_save = adding_data.encode('utf-8') + data
        else:
            data_save = data
        field = new_obj.getField(field_name)
        if data_save:
            field.set(new_obj, data_save)
        if filename is not None:
            if field_dic.get('is_blob', False):
                field.getRaw(new_obj).setFilename(filename)
            else:
                field.setFilename(new_obj, filename)
        if contenttype is not None:
            field.setContentType(new_obj, contenttype)
    new_obj._renameAfterCreation(check_auto_id=True)
    return new_obj

def set_field_dx_types(obj, new_obj, request):
    title = None
    for field_dic in _copy_dx_fields(obj):
        field_name = field_dic['field_name']
        data  = field_dic.get('data', '')
        if field_name == 'title':
            adding_data = translate(ADDING_TITLE, context=request)
            if isinstance(data, unicode):
                data_save = adding_data + data
            else:
                data_save = adding_data.encode('utf-8') + data
            title = data_save
        else:
            data_save = data
        if data_save:
            setattr(new_obj, field_name, data_save)
    if title is not None:
        oid = INameChooser(aq_parent(new_obj)).chooseName(title, new_obj)
        aq_parent(new_obj).manage_renameObject(new_obj.id, oid)
    return new_obj


class ContentPaste(BrowserView):
    
    def __call__(self):
        msg = ""
        try:
            new_obj = self.create_new_obj()
        except ConflictError:
            raise
        except (Unauthorized, 'Unauthorized'):
            msg = _(u'Unauthorized to paste item(s).')
        except: # fallback
            msg = _(u'New content could not create for duplicate.')
        if msg:
            self.context.plone_utils.addPortalMessage(msg, 'error')
            raise

        msg = _(u"Duplicate new content")
        self.context.plone_utils.addPortalMessage(msg, 'info')
        self.context.REQUEST.RESPONSE.redirect(new_obj.absolute_url() + '/edit')
        return None
    
    def create_new_obj(self):
        container = aq_parent(self.context)
        obj = self.context
        new_id = _generate_unique_id(obj.portal_type)
        new_obj_id = container.invokeFactory(obj.portal_type, new_id)
        transaction.savepoint(optimistic=True)
        new_obj = getattr(container, new_obj_id)
        if IATContentType in providedBy(obj):
            new_obj = set_field_at_types(obj, new_obj, self.request)
        elif DEXTERITY_INSTALLED and IDexterityContent in providedBy(obj):
            new_obj = set_field_dx_types(obj, new_obj, self.request)
        new_obj.reindexObject()

        return new_obj
