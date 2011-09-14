# -*- coding:utf-8 -*-
from Acquisition import aq_inner
from five import grok
from plone.directives import dexterity, form

from zope import schema

from zope.schema.interfaces import IVocabularyFactory
from zope.component import getMultiAdapter, queryUtility


from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds

from plone.indexer import indexer

from z3c.form import group, field
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

from apyb.registration import MessageFactory as _

class IAttendee(form.Schema):
    """
    An attenddee at a conference
    """
    form.omitted('uid')
    uid = schema.Int(
        title=_(u"uid"),
        required=False,
        )
    
    registration_type = schema.Choice(
        title=_(u'Type'),
        description=_(u'Select the category of your registration'),
        required=False,
        vocabulary="apyb.registration.types"
    )
    
    fullname = schema.TextLine(
        title=_(u'Fullname'),
        description=_(u'Please inform your fullname'),
        required=True,
    )
    
    badge_name = schema.TextLine(
        title=_(u'Badge name'),
        description=_(u'Please inform the name that will appear on your badge -- Leave it blank to use your fullname in the badge'),
        required=False,
        missing_value=u'',
    )
    
    organization = schema.TextLine(
        title=_(u'Organization'),
        description=_(u'Please inform the name of the organization you will represent'),
        required=False,
        missing_value=u'',
    )
    
    gender = schema.Choice(
        title=_(u'Gender'),
        required=True,
        vocabulary="apyb.registration.gender"
        )

    t_shirt_size = schema.Choice(
        title=_(u'T-Shirt Size'),
        required=True,
        vocabulary="apyb.registration.tshirt"
        )


class Attendee(dexterity.Item):
    grok.implements(IAttendee)
    
    def _get_title(self):
        return self.fullname
    def _set_title(self, value):
        pass
    title = property(_get_title, _set_title)
    
    def Title(self):
        return self.title
    
    @property
    def uid(self):
        intids = getUtility(IIntIds)
        return intids.getId(self)
    
    def UID(self):
        return self.uid

@indexer(IAttendee)
def registration_type(obj):
    return [obj.registration_type,]
grok.global_adapter(registration_type, name="Subject")


class View(grok.View):
    grok.context(IAttendee)
    grok.require('zope2.View')
    
    def update(self):
        super(View,self).update()
        context = aq_inner(self.context)
        self.registration_type = self.context.registration_type
        self._path = '/'.join(context.getPhysicalPath())
        self.state = getMultiAdapter((context, self.request), name=u'plone_context_state')
        self.tools = getMultiAdapter((context, self.request), name=u'plone_tools')
        self.portal = getMultiAdapter((context, self.request), name=u'plone_portal_state')
        self._ct = self.tools.catalog()
        self.member = self.portal.member()
        self.voc = queryUtility(IVocabularyFactory, 'apyb.registration.types')(context)
        roles_context = self.member.getRolesInContext(context)
        if not [r for r in roles_context if r in ['Manager','Editor','Reviewer',]]:
            self.request['disable_border'] = True
    
    @property
    def fmt_registration_type(self):
        registration_type = self.registration_type
        if registration_type:
            return self.voc.getTerm(registration_type).title
