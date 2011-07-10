from five import grok
from plone.directives import dexterity, form

from zope import schema

from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds

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


class View(grok.View):
    grok.context(IAttendee)
    grok.require('zope2.View')
    
