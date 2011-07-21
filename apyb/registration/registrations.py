# -*- coding:utf-8 -*-
from five import grok

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from zope.schema.interfaces import IVocabularyFactory
from zope.component import getMultiAdapter, queryUtility

from plone.directives import dexterity, form

from zope import schema

from z3c.form import group, field
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

from apyb.registration import MessageFactory as _


# Interface class; used to define content-type schema.

class IRegistrations(form.Schema):
    """
    Folderish content that contains registrations
    """
    

class Registrations(dexterity.Container):
    grok.implements(IRegistrations)
    
    
class View(grok.View):
    grok.context(IRegistrations)
    grok.require('zope2.View')
    
    def update(self):
        context = aq_inner(self.context)
        self._path = '/'.join(context.getPhysicalPath())
        self.state = getMultiAdapter((context, self.request), name=u'plone_context_state')
        self.tools = getMultiAdapter((context, self.request), name=u'plone_tools')
        self.portal = getMultiAdapter((context, self.request), name=u'plone_portal_state')
        self._ct = self.tools.catalog()
        self.is_anonymous = self.portal.anonymous()
        self.mt = self.tools.membership()
        if not self.show_border:
            self.request['disable_border'] = True
    
    @property
    def vocabs(self):
        if not hasattr(self, "_vocabs"):
            vocabs = {}
            vocabs['gender'] = queryUtility(IVocabularyFactory, 'apyb.registration.gender')
            vocabs['tshirt'] = queryUtility(IVocabularyFactory, 'apyb.registration.tshirt')
            vocabs['types'] = queryUtility(IVocabularyFactory, 'apyb.registration.types')
            vocabs['payment'] = queryUtility(IVocabularyFactory, 'apyb.registration.paymentservices')
            vocabs['country'] = queryUtility(IVocabularyFactory, 'contact.countries')
            self._vocabs = dict((key,value(self)) for key, value in vocabs.items())
        return self._vocabs
    
    @property
    def login_url(self):
        return '%s/login' % self.portal.portal_url()
    
    @property
    def register_url(self):
        return '%s/@@register' % self.portal.portal_url()
    
    @property
    def registrations_enabled(self):
        mt = self.mt
        state = self.state.workflow_state()
        # If opened, its enabled
        if state == 'opened':
            return True
        return mt.checkPermission('apyb.registration: Add Registration',self.context)
    
    def registration_options(self):
        base = self.context.absolute_url()
        options = [
                   {'type':'apyb','href':'%s/@@registration-apyb' % base,'text':_(u'Register as an APyB Member'),},
                   {'type':'student','href':'%s/@@registration-student' % base,'text':_(u'Register as a student'),},
                   {'type':'individual','href':'%s/@@registration-individual' % base,'text':_(u'Register as an Individual'),},
                   {'type':'group','href':'%s/@@registration-group' % base,'text':_(u'Register members of a group or organization (Group registration)'),},
                   {'type':'government','href':'%s/@@registration-gov' % base,'text':_(u'Register member(s) of Brazilian Government'),},
                  ]
        return options
    
    @property
    def show_border(self):
        ''' Is this user allowed to edit this content '''
        return self.state.is_editable()
    
    @property
    def listing_enabled(self):
        ''' Is this user allowed to view registration listings '''
        return self.show_border
    
    def _regs_as_dict(self,registrations):
        ''' Given a list of brains, we return proper dictionaries '''
        voc = self.vocabs
        regs = []
        for brain in registrations:
            reg = {}
            reg['id'] = brain.getId
            reg['url'] = brain.getURL()
            reg['email'] = brain.email
            reg['date'] = brain.created
            reg['title'] = brain.Title
            reg['type'] = voc['types'].getTerm(brain.Subject[0]).title
            reg['num_attendees'] = brain.num_attendees
            reg['price_est'] = brain.price_est
            reg['amount'] = brain.amount
            reg['state'] = brain.review_state
            regs.append(reg)
        return regs
    
    def _att_as_dict(self,attendees):
        ''' Given a list of brains, we return proper dictionaries '''
        voc = self.vocabs
        atts = []
        for brain in attendees:
            att = {}
            att['id'] = brain.getId
            att['reg'] = brain.getPath().split('/')[-2]
            att['url'] = brain.getURL()
            att['date'] = brain.created
            att['fullname'] = brain.Title
            att['email'] = brain.email
            att['badge_name'] = brain.badge_name or att['fullname']
            att['gender'] = voc['gender'].getTerm(brain.gender).title
            att['t_shirt_size'] = voc['tshirt'].getTerm(brain.t_shirt_size).title
            att['state'] = brain.review_state
            atts.append(att)
        return atts
    
    def registrations(self):
        ''' List registrations'''
        ct = self._ct
        results = ct.searchResults(portal_type='apyb.registration.registration',
                                   path=self._path)
        return self._regs_as_dict(results)
    
    def attendees(self):
        ''' List attenddees'''
        ct = self._ct
        results = ct.searchResults(portal_type='apyb.registration.attendee',
                                   path=self._path)
        return self._att_as_dict(results)
    

    