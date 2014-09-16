# -*- coding: utf-8 -*-
from . import _
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, DateTime, Unicode, UnicodeText, Boolean

Base = declarative_base()


"""
    Form definition
    ----------------- 
     f[0]: fieldname
     f[1]: fieldlabel
     f[3]: field wrapper (see email)
     f[4]: Filedtype: Text, TextLine
     f[5]: True = visible for everybody, False = only for himself
"""

TABLE_EXTUSERPROFILE = 'extended_userprofiles' 

FIELDSETS = {
    'FIELDSET_00' : [
        ('acadtitle',_('Academic title'),'','','TextLine','True'),
        ('firstname',_('Firstname'),'','','TextLine','True'), 
        ('lastname',_('Lastname'),'','', 'TextLine','True'), 
        ('birthdate', _('Day of Birth'), '', '', 'Date','True'), 
        ('homecity', _('Home City'), '', '', 'TextLine','True'),
        ],    
    'FIELDSET_01' : [
        ('street',_('street & no.'),'','','TextLine','True'), 
        ('city',_('city'),'','', 'TextLine','True'), 
        ('country',_('country'),'','', 'TextLine','True'),
        ('home_page',_('home_page'),'http://','', 'TextLine','True'),
        ],
    'FIELDSET_02' : [
        ('phone',_('Phone number'),'','', 'TextLine','True'), 
        ('fax',_('Fax number'),'','', 'TextLine','True'),
        ('email',_('Email'),'icon','mailto:%s', 'TextLine','True'),
        ('imessage_notifies',_('E-Mail notifies for new messages'),'','', 'CheckBox','False'), 
        ('skype',_('Skype'),'icon','skype:%s?call', 'TextLine','True'),
        ('xing',_('Xing'),'icon','', 'TextLine','True'),
        ('linkedin',_('LinkedIn'),'icon','', 'TextLine','True'),
        ('fb',_('Facebook'),'icon','', 'TextLine','True'),
        ('twitter',_('Twitter'),'icon','', 'TextLine','True'),
        ('icq',_('ICQ'),'icon','', 'TextLine','True'),
        ],
    'FIELDSET_03' : [
        ('department', _('Department'), '', '', 'TextLine','True'),
        ('position', _('Position'), '', '', 'TextLine','True'),
        ('superior', _('Superior'), '', '', 'TextLine','True'),  
        ('location', _('Location'), '', '', 'TextLine','True'),
        ],

    'FIELDSET_04' : [
        ('education', _('Education'), '', '', 'Text','True'), 
        ('profession', _('Profession'), '', '', 'Text','True'),
        ],
    'FIELDSET_05' : [
        ('description', _('Description'), '', '', 'Text','True'),
        ],
    'FIELDSET_06' : [
        ('leasure', _('Favorite activities'), '', '', 'Text','True'),
        ('like', _('I like'), '', '', 'Text','True'),
        ('dislike', _('I dislike'), '', '', 'Text','True'),
        ('demands', _('I am looking for'), '', '', 'Text','True'),
        ('offers', _('I offer'), '', '', 'Text','True'),
        ],
    }

class ExtendedUserProfile(Base):
    """ Extendes User Profile. The extended user properties are
        stored in an sql-Database.
    """
    
    __tablename__ = TABLE_EXTUSERPROFILE

    id          = Column(Unicode, primary_key=True)
    salutation  = Column(Unicode)
    acadtitle   = Column(Unicode)
    firstname   = Column(Unicode)
    lastname    = Column(Unicode)
    
    birthdate   = Column(Date)
    homecity    = Column(Unicode)
    
    leasure     = Column(UnicodeText)
    like        = Column(UnicodeText)
    dislike     = Column(UnicodeText)
    
    education   = Column(UnicodeText)
    profession  = Column(UnicodeText)
    
    phone       = Column(Unicode)
    fax         = Column(Unicode)
    skype       = Column(Unicode)
    xing        = Column(Unicode)
    linkedin    = Column(Unicode)
    fb          = Column(Unicode)
    twitter     = Column(Unicode)
    icq         = Column(Unicode)
    
    street      = Column(Unicode)
    city        = Column(Unicode)
    country     = Column(Unicode)
     
    department  = Column(Unicode)
    position    = Column(Unicode)
    superior    = Column(Unicode)
     
    demands     = Column(UnicodeText)
    offers      = Column(UnicodeText)
    
    timestamp   = Column(DateTime)
    imessage_notifies = Column(Boolean)

