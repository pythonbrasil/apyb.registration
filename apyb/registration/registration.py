from five import grok
from plone.directives import dexterity, form

from Acquisition import aq_inner, aq_parent

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
    
    email = schema.TextLine(
           title=_(u'E-mail'),
           description=_(u'Please provide an email address'),
           required=True,
    )
    
    registration_type = schema.Choice(
        title=_(u'Type'),
        description=_(u'Select the category of your registration'),
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
    
    def attendees(self):
        ct = self.context.portal_catalog
        path = '/'.join(self.context.getPhysicalPath())
        results = ct.searchResults(portal_type='apyb.registration.attendee',path=path)
        return results
    
    @property
    def paid(self):
        return getattr(self.context,'paid',False)
    
    @property
    def show_pagseguro(self):
        ''' show only if registration not paid and 
            registration is from brazil
        '''
        country = self.context.country
        paid = self.paid
        return (country==u'br' and not paid)
    
    @property
    def show_paypal(self):
        ''' show only if registration not paid 
        '''
        paid = self.paid
        return paid
    
    def _price(self):
        view = aq_parent(self.context).restrictedTraverse('@@reg-price')
        attendees = self.attendees()
        qty = len(attendees)
        registration_type = self.context.registration_type
        price = view.price(registration_type,qty)
        fmtPrice = view.fmtPrice(price)
        return (price,fmtPrice)
    
    @property
    def price(self):
        return self._price()[0]
        
    @property
    def fmtPrice(self):
        return self._price()[1]

    

        