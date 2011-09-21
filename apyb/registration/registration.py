from five import grok
from plone.directives import dexterity, form

from Acquisition import aq_inner, aq_parent

from zope.schema.interfaces import IVocabularyFactory
from zope.component import getMultiAdapter, queryUtility

from zope import schema

from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds

from plone.memoize.view import memoize

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
    #
    email = schema.TextLine(
           title=_(u'E-mail'),
           description=_(u'Please provide an email address'),
           required=True,
    )
    #
    registration_type = schema.Choice(
        title=_(u'Type'),
        description=_(u'Select the category of your registration'),
        required=True,
        vocabulary="apyb.registration.types",
        )
    #
    discount_code = schema.TextLine(
        title=_(u'Discount code'),
        description=_(u'If you have a discount code, please inform here'),
        required=False,
        missing_value=u'',
    )


@indexer(IRegistration)
def num_attendees(obj):
    children = obj.objectValues()
    children = [c for c in children
                        if c.portal_type=='apyb.registration.attendee']
    return len(children)
grok.global_adapter(num_attendees, name="num_attendees")


@indexer(IRegistration)
def price_est(obj):
    if not getattr(obj, 'paid', False):
        children = obj.objectValues()
        children = [c for c in children
                            if c.portal_type=='apyb.registration.attendee']
        #
        view = aq_parent(obj).restrictedTraverse('@@reg-price')
        qty = len(children)
        #
        registration_type = obj.registration_type
        discount_code = obj.discount_code
        price = view.price(registration_type, qty, discount_code)
    else:
        price = obj.amount
    return price

grok.global_adapter(price_est, name="price_est")


@indexer(IRegistration)
def registration_type(obj):
    return [obj.registration_type, ]
grok.global_adapter(registration_type, name="Subject")


class Registration(dexterity.Container):
    grok.implements(IRegistration)
    #
    def __init__(self, id=None, **kwargs):
        if not id:
            id = generateId()
        super(Registration, self).__init__(id=id, **kwargs)
    #
    @property
    def uid(self):
        intids = getUtility(IIntIds)
        return intids.getId(self)
    #
    def UID(self):
        return self.uid


class View(grok.View):
    grok.context(IRegistration)
    grok.require('zope2.View')
    #
    def update(self):
        super(View, self).update()
        context = aq_inner(self.context)
        registrations = aq_parent(self.context)
        self.registration_type = context.registration_type
        self._path = '/'.join(context.getPhysicalPath())
        self.state = getMultiAdapter((context, self.request),
                                      name=u'plone_context_state')
        self.tools = getMultiAdapter((context, self.request),
                                      name=u'plone_tools')
        self.portal = getMultiAdapter((context, self.request),
                                       name=u'plone_portal_state')
        self.helper = getMultiAdapter((registrations, self.request),
                                      name=u'helper')
        self._ct = self.tools.catalog()
        self._mt = self.tools.membership()
        self.member = self.portal.member()
        self.price_view = registrations.restrictedTraverse('@@reg-price')
        voc_factory = queryUtility(IVocabularyFactory,
                                   'apyb.registration.types')
        self.voc = voc_factory(context)
        self.roles_context = self.member.getRolesInContext(context)
        url = context.absolute_url()
        self.training_form = '%s/@@registration-training' % url
        if not [r for r in self.roles_context
                        if r in ['Manager', 'Editor', 'Reviewer', ]]:
            self.request['disable_border'] = True
    #
    def attendees(self):
        ct = self._ct
        path = self._path
        results = ct.searchResults(portal_type='apyb.registration.attendee',
                                   path=path)
        return results

    def attendee(self, attendee_uid):
        ct = self._ct
        results = ct.searchResults(UID=attendee_uid)
        if results:
            brain = results[0]
            return brain.getObject()
    #
    @property
    def creator(self):
        creator = self.context.Creator()
        data = []
        if isinstance(creator, str):
            creator = [creator, ]
        for member_id in creator:
            member = self._mt.getMemberById(member_id)
            if member:
                member_fullname = member.getProperty('fullname') or member_id
                member_email = member.getProperty('email') or member_id
                member = '%s <%s>' % (member_fullname, member_email)
            else:
                member = member_id
            data.append(member)
        return ', '.join(data)
    #
    @property
    def created(self):
        created = self.context.creation_date
        return created.strftime('%d/%m/%Y %H:%M')
    #
    @property
    def fmt_registration_type(self):
        registration_type = self.registration_type
        term = self.voc.getTerm(registration_type)
        return term.title
    #
    @property
    def show_payments(self):
        state = self.state.workflow_state()
        return not (self.paid or state == 'confirmed')
    #
    @property
    def paid(self):
        is_paid = getattr(self.context, 'paid', False)
        if self.registration_type in ['organizer', 'sponsor']:
            is_paid = True
        return is_paid
    #
    @property
    def price_paid(self):
        view = self.price_view
        amount = self.context.amount
        fmtPrice = view.fmtPrice(amount)
        return fmtPrice
    #
    @property
    def show_empenho(self):
        ''' show only if registration type == government'''
        return self.registration_type == 'government'
    #
    @property
    def show_pagseguro(self):
        ''' show only if registration not paid and
            registration is from brazil
        '''
        country = self.context.country
        paid = self.paid
        return (country == u'br' and not (paid or self.show_empenho))
    #
    @property
    def show_paypal(self):
        ''' show only if registration not paid
        '''
        paid = self.paid
        return not (paid or self.show_empenho)
    #
    def _price(self):
        view = self.price_view
        attendees = self.attendees()
        qty = len(attendees)
        registration_type = self.registration_type
        discount_code = self.context.discount_code
        price = view.price(registration_type, qty, discount_code)
        fmtPrice = view.fmtPrice(price)
        return (price, fmtPrice)
    #
    @property
    def base_price(self):
        # Price per attendee
        attendees = self.attendees()
        qty = len(attendees) or 1
        price = self._price()[0]
        return price / qty
    #
    @property
    def price(self):
        return self._price()[0]
    #
    @property
    def fmtBasePrice(self):
        return self.price_view.fmtPrice(self.base_price)
    #
    @property
    def fmtPrice(self):
        return self._price()[1]
    #
    def available_trainings(self):
        ''' List of available trainings '''
        helper = self.helper
        return helper.trainings()
