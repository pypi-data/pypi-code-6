from zope.component import adapts

from Products.CMFCore.permissions import ModifyPortalContent
from Products.PloneFormGen.content.formMailerAdapter import FormMailerAdapter
from Products.PloneFormGen import PloneFormGenMessageFactory as _
from Products.Archetypes.atapi import AnnotationStorage, ATFieldProperty

from raptus.multilanguagefields import widgets
from raptus.multilanguageplone.extender import fields
from raptus.multilanguageplone.extender.base import DefaultExtender


class FormMailerAdapterExtender(DefaultExtender):

    adapts(FormMailerAdapter)

    FROM_BASE_SCHEMA = ('title','description',)
    
    fields = [
              
        fields.StringField('msg_subject',
            schemata='message',
            searchable=False,
            required=False,
            accessor='getMsg_subject',
            default='Form Submission',
            read_permission=ModifyPortalContent,
            storage=AnnotationStorage(migrate=True),
            widget=widgets.StringWidget(
                description=_(u'help_formmailer_subject',
                    default=u"""
                    Subject line of message. This is used if you
                    do not specify a subject field or if the field
                    is empty.
                    """),
                label=_(u'label_formmailer_subject', default=u'Subject'),
                ),
            ),
              
        fields.TextField('body_pre',
            searchable=False,
            required=False,
            schemata='message',
            accessor='getBody_pre',
            read_permission=ModifyPortalContent,
            storage=AnnotationStorage(migrate=True),
            default_content_type='text/plain',
            allowable_content_types=('text/plain',),
            widget=widgets.TextAreaWidget(description=_(u'help_formmailer_body_pre',
                          default=u'Text prepended to fields listed in mail-body'),
              label=_(u'label_formmailer_body_pre', default=u'Body (prepended)'),
                ),
            ),
              
        fields.TextField('body_post',
            searchable=False,
            required=False,
            schemata='message',
            read_permission=ModifyPortalContent,
            storage=AnnotationStorage(migrate=True),
            default_content_type='text/plain',
            allowable_content_types=('text/plain',),
            widget=widgets.TextAreaWidget(description=_(u'help_formmailer_body_post',
                          default=u'Text appended to fields listed in mail-body'),
              label=_(u'label_formmailer_body_post', default=u'Body (appended)'),
                ),
            ),
    
        fields.TextField('body_footer',
            searchable=False,
            required=False,
            schemata='message',
            read_permission=ModifyPortalContent,
            storage=AnnotationStorage(migrate=True),
            default_content_type='text/plain',
            allowable_content_types=('text/plain',),
            widget=widgets.TextAreaWidget(description=_(u'help_formmailer_body_footer',
                              default=u'Text used as the footer at '
                              u'bottom, delimited from the body by a dashed line.'),
                label=_(u'label_formmailer_body_footer',
                          default=u'Body (signature)'),
                ),
            ),
        ]

        
    fields = fields + [f for f in DefaultExtender.fields if f.getName() in FROM_BASE_SCHEMA]
   
    # Set AT field property fields for all extended fields.
    FormMailerAdapter.msg_subject = ATFieldProperty('msg_subject')
    FormMailerAdapter.body_pre = ATFieldProperty('body_pre')
    FormMailerAdapter.body_post = ATFieldProperty('body_post')
    FormMailerAdapter.body_footer = ATFieldProperty('body_footer')