from zope.formlib import form
from zope.interface import implements
from zope.component import adapts
import zope.lifecycleevent
from zope.component import getMultiAdapter

from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from plone.app.form import base as ploneformbase

from medialog.simpleslider.interfaces import ISimplesliderSettings 
from medialog.simpleslider import simplesliderMessageFactory as _
from medialog.simpleslider.settings import SimplesliderSettings
  

class SimplesliderSettingsForm(ploneformbase.EditForm):
    """
    The page that holds all the settings
    """
    form_fields = form.FormFields(ISimplesliderSettings)
      
    label = _(u'heading_simpleslider_settings_form', default=u"Simpleslider Settings")
    description = _(u'description_simpleslider_settings_form', default=u"Configure the parameters for this file.")
    form_name = _(u'title_simpleslider_settings_form', default=u"Simpleslider settings")
    
    