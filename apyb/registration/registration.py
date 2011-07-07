from five import grok
from plone.directives import dexterity, form

from zope import schema

from z3c.form import group, field
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds

from apyb.registration.utils import generateId

from apyb.registration import MessageFactory as _

class IRegistration(form.Schema):
    """
    A registration in a conference
    """
    form.omitted('uid')
    uid = schema.Int(
        title=_(u"uid"),
        required=False,
        )
    registration_type = schema.Choice(
        title=_(u'Type'),
        required=True,
        vocabulary="apyb.registration.types"
        )
    
    discount_code = schema.TextLine(
        title=_(u'Discount code'),
        description=_(u'If you have a discount code, please inform here'),
        required=False,
        missing_value=u'',
    )


class Registration(dexterity.Container):
    grok.implements(IRegistration)
    
    def __init__(self, id=None, **kwargs):
        if not id:
            id = generateId()
        super(Registration,self).__init__(id=id, **kwargs)
    
    @property
    def uid(self):
        intids = getUtility(IIntIds)
        return intids.getId(self)


class View(grok.View):
    grok.context(IRegistration)
    grok.require('zope2.View')
    