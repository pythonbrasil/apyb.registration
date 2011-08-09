from five import grok
from plone.directives import dexterity, form

from Acquisition import aq_inner, aq_parent

from zope.component import getMultiAdapter

from zope import schema

from z3c.form import group, field
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds

from plone.indexer import indexer

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


@indexer(IRegistration)
def num_attendees(obj):
    children = obj.objectValues()
    children = [c for c in children if c.portal_type=='apyb.registration.attendee']
    return len(children)
grok.global_adapter(num_attendees, name="num_attendees")

@indexer(IRegistration)
def price_est(obj):
    if not getattr(obj,'paid',False):
        children = obj.objectValues()
        children = [c for c in children if c.portal_type=='apyb.registration.attendee']
        
        view = aq_parent(obj).restrictedTraverse('@@reg-price')
        qty = len(children)
        
        registration_type = obj.registration_type
        discount_code = obj.discount_code
        price = view.price(registration_type,qty,discount_code)
    else:
        price = obj.amount
    return price

grok.global_adapter(price_est, name="price_est")

@indexer(IRegistration)
def registration_type(obj):
    return [obj.registration_type,]
grok.global_adapter(registration_type, name="Subject")

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
    
    def update(self):
        super(View,self).update()
        context = aq_inner(self.context)
        self.registration_type = context.registration_type
        self._path = '/'.join(context.getPhysicalPath())
        self.state = getMultiAdapter((context, self.request), name=u'plone_context_state')
        self.tools = getMultiAdapter((context, self.request), name=u'plone_tools')
        self.portal = getMultiAdapter((context, self.request), name=u'plone_portal_state')
        self._ct = self.tools.catalog()
        self.member = self.portal.member()
        roles_context = self.member.getRolesInContext(context)
        if not [r for r in roles_context if r in ['Manager','Editor','Reviewer',]]:
            self.request['disable_border'] = True
    
    def attendees(self):
        ct = self._ct
        path = self._path
        results = ct.searchResults(portal_type='apyb.registration.attendee',path=path)
        return results

    @property
    def show_payments(self):
        state = self.state.workflow_state()
        return not (self.paid  or state == 'confirmed')
    
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
        return not paid
    
    def _price(self):
        view = aq_parent(self.context).restrictedTraverse('@@reg-price')
        attendees = self.attendees()
        
        qty = len(attendees)
        registration_type = self.registration_type
        discount_code = self.context.discount_code
        price = view.price(registration_type,qty, discount_code)
        fmtPrice = view.fmtPrice(price)
        return (price,fmtPrice)
    
    @property
    def base_price(self):
        # Price per attendee
        attendees = self.attendees()
        qty = len(attendees)
        price = self._price()[0]
        return price / qty
    
    @property
    def price(self):
        return self._price()[0]
        
    @property
    def fmtPrice(self):
        return self._price()[1]

    

        