# -*- coding:utf-8 -*-
from five import grok
from zope import component
from zope.app.intid.interfaces import IIntIds
from z3c.form import button, field, group
from z3c.form.interfaces import HIDDEN_MODE
from z3c.form.form import applyChanges
from z3c.form.interfaces import IWidgets
from plone.dexterity.utils import createContentInContainer
from plone.directives import form

from apyb.registration.behavior.optininformation import IOptInInformation
from collective.behavior.contactinfo.behavior.contactinfo import INetContactInfo
from collective.behavior.contactinfo.behavior.address import IAddress

from apyb.registration.registration import IRegistration
from apyb.registration.attendee import IAttendee
from apyb.registration.registrations import IRegistrations

from apyb.registration import MessageFactory as _

class TicketGroup(group.Group):
    label=u"Ticket Type"
    description=u"Please select your price."
    fields=field.Fields(IRegistration).select(
        'registration_type',
        )

class AttendeeGroup(group.Group):
    label=u"Personal"
    description=u"Please inform your personal data for registration."
    fields=field.Fields(IAttendee).omit('uid')
    fields = fields + field.Fields(INetContactInfo)

class LocaleGroup(group.Group):
    label=u"Location"
    description=u"Where are you from?"
    fields = field.Fields(IAddress).select('country','state','city')
    
    def updateWidgets(self):
        super(LocaleGroup, self).updateWidgets()
        self.widgets['country'].field.default='br'
    

class OptInGroup(group.Group):
    label=u"OptIn"
    description=u"OptIn."
    fields=field.Fields(IOptInInformation)

class DiscountGroup(group.Group):
    label=u"Discount code"
    description=u"Please select your price."
    fields=field.Fields(IRegistration).select(
        'discount_code',
    )

class RegistrationForm(group.GroupForm, form.Form):
    grok.name('registration')
    grok.require('apyb.registration.AddRegistration')
    grok.context(IRegistrations)
    
    fields=field.Fields(IRegistration).select('uid')
    
    groups = (TicketGroup, AttendeeGroup, LocaleGroup, DiscountGroup, OptInGroup,)
    
    label = _(u"Register")
    enable_form_tabbing = False
    
    def update(self):
        # disable Plone's editable border
        self.request.set('disable_border', True)
        if not self.request.get('form.widgets.country',''):
            self.request.set('form.widgets.country','br')
        self.ignoreContext = True
        super(RegistrationForm, self).update()

    def updateWidgets(self):
        super(RegistrationForm, self).updateWidgets()
        self.widgets['uid'].mode = HIDDEN_MODE
    
    @button.buttonAndHandler(u'Register')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        reg_fields = ['registration_type','discount_code',]
        reg_data = dict([(k,data[k]) for k in reg_fields])
        registration = createContentInContainer(self.context, 'apyb.registration.registration', 
                                                checkConstraints=True, **reg_data)
        
        for k in reg_fields + ['uid']:
            del data[k]
        attendee = createContentInContainer(registration, 'apyb.registration.attendee', 
                                                checkConstraints=True, **data)
