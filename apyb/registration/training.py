# -*- coding:utf-8 -*-
from Acquisition import aq_inner
from Acquisition import aq_parent
from five import grok
from plone.directives import dexterity, form

from plone.memoize.view import memoize

from zope import schema

from zope.schema.interfaces import IVocabularyFactory
from zope.component import getMultiAdapter, queryUtility


from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds

from Products.CMFCore.interfaces import ISiteRoot

from apyb.registration.utils import generateId

from apyb.registration import MessageFactory as _


class ITrainingRegistration(form.Schema):
    """
    A registration to a training in a conference
    """
    form.omitted('uid')
    uid = schema.Int(
        title=_(u"uid"),
        required=False,
        )
    #
    attendee = schema.Choice(
        title=_(u'Attendee'),
        description=_(u'Select the attendee'),
        required=True,
        vocabulary="apyb.registration.attendees_registration",
    )
    #
    form.widget(trainings='z3c.form.browser.checkbox.CheckBoxFieldWidget')
    trainings = schema.List(
        title=_(u'Trainings'),
        description=_(u'Select trainings'),
        default=[],
        value_type=schema.Choice(title=_(u"Training"),
                                 vocabulary='apyb.registration.trainings'),
        required=False,
    )
    #


class TrainingRegistration(dexterity.Item):
    #
    grok.implements(ITrainingRegistration)
    #
    def __init__(self, id=None, **kwargs):
        if not id:
            id = generateId()
        super(TrainingRegistration, self).__init__(id=id, **kwargs)
    #
    def _get_title(self):
        attendee_uid = self.attendee
        portal = getUtility(ISiteRoot)
        factory = queryUtility(IVocabularyFactory,
                               'apyb.registration.attendees_registration')
        vocab = factory(portal)
        vocab_item = vocab.getTerm(attendee_uid)
        attendee_name = vocab_item.title
        return 'training-%s' % attendee_name
    #
    def _set_title(self, value):
        pass
    #
    title = property(_get_title, _set_title)
    #
    def Title(self):
        return self.title
    #
    @property
    def uid(self):
        intids = getUtility(IIntIds)
        return intids.getId(self)
    #
    def UID(self):
        return self.uid


class AddForm(dexterity.AddForm):
    grok.name('apyb.registration.training')
    grok.require('apyb.registration.AddTrainingRegistration')
    #
    def create(self, data):
        content = super(AddForm, self).create(data)
        return content


class View(grok.View):
    grok.context(ITrainingRegistration)
    grok.require('zope2.View')
    #
    def update(self):
        super(View, self).update()
        context = aq_inner(self.context)
        registration = aq_parent(context)
        registrations = aq_parent(registration)
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
        self.member = self.portal.member()
        voc_factory = queryUtility(IVocabularyFactory,
                                   'apyb.papers.talk.rooms')
        self.rooms = voc_factory(self.context)
        self.roles_context = self.member.getRolesInContext(context)
        if not [r for r in self.roles_context
                        if r in ['Manager', 'Editor', 'Reviewer', ]]:
            self.request['disable_border'] = True
    @property
    def attendee(self):
        attendee_uid = self.context.attendee
        ct = self._ct
        results = ct.searchResults(UID=attendee_uid)
        if results:
            brain = results[0]
            return brain.getObject()
    
    @property
    def fullname(self):
        attendee = self.attendee
        return attendee.fullname
    #
    @memoize
    def trainings(self):
        helper = self.helper
        program_helper = helper.program_helper
        return program_helper.trainings_dict

    @memoize
    def speakers(self):
        helper = self.helper
        program_helper = helper.program_helper
        return program_helper.speakers_dict

    def training_info(self, training_uid):
        trainings = self.trainings()
        return trainings.get(training_uid, {})

    def speaker_name(self, speakers_uid):
        speakers = self.speakers()
        return ','.join([speakers.get(uid, {'name': '',})['name'] 
                                      for uid in speakers_uid])

    def location(self, location_uid):
        rooms = self.rooms
        try:
            term = rooms.getTerm(location_uid)
        except LookupError:
            return location_uid
        return term.title

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
        trainings = self.trainings
        qty = len(trainings)
        registration_type = 'training'
        discount_code = ''
        price = view.price(registration_type, qty, discount_code)
        fmtPrice = view.fmtPrice(price)
        return (price, fmtPrice)
    #
    @property
    def base_price(self):
        # Price per attendee
        trainings = self.trainings
        qty = len(trainings) or 1
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