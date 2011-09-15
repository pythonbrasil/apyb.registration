# -*- coding:utf-8 -*-
from five import grok

from Acquisition import aq_inner

from zope.component import getMultiAdapter

from plone.memoize.view import memoize

from apyb.registration.config import PROGRAM_PATH

from apyb.registration.registrations import IRegistrations


class View(grok.View):
    grok.context(IRegistrations)
    grok.require('zope2.View')
    grok.name('helper')
    #
    def __init__(self, context, request):
        super(View, self).__init__(context, request)
        context = aq_inner(self.context)
        self._path = '/'.join(context.getPhysicalPath())
        self.state = getMultiAdapter((context, self.request),
                                      name=u'plone_context_state')
        self.tools = getMultiAdapter((context, self.request),
                                      name=u'plone_tools')
        self.portal = getMultiAdapter((context, self.request),
                                      name=u'plone_portal_state')
        portal = self.portal.portal()
        self.program = portal.restrictedTraverse(PROGRAM_PATH)
        self.program_helper = getMultiAdapter((self.program, self.request),
                                               name=u'helper')
        self._ct = self.tools.catalog()
    #
    def render(self):
        return ''
    #
    @memoize
    def registrations(self, **kw):
        kw['portal_type'] = 'apyb.registration.registration'
        kw['path'] = self._path
        brains = self._ct.searchResults(**kw)
        return brains
    #
    @memoize
    def attendees(self, **kw):
        kw['portal_type'] = 'apyb.registration.attendee'
        if not 'path' in kw:
            kw['path'] = self._path
        brains = self._ct.searchResults(**kw)
        return brains
    #
    @memoize
    def training_registrations(self, **kw):
        kw['portal_type'] = 'apyb.registration.training'
        if not 'path' in kw:
            program_path = '/'.join(self.program.getPhysicalPath())
            kw['path'] = program_path
        brains = self._ct.searchResults(**kw)
        return brains
    #
    @property
    def registrations_dict(self):
        brains = self.registrations()
        regs = dict([(b.UID, {'title': b.Title,
                               'email': b.email,
                               'review_state': b.review_state,
                               'type': b.Subject and b.Subject[0],
                               'paid': b.paid,
                               'amount': b.amount,
                               'price': b.price,
                               'num_attendees':b.num_attendees,
                               'url': b.getURL(),
                               'json_url': '%s/json' % b.getURL(), })
                    for b in brains])
        return regs
    #
    @property
    def attendees_dict(self):
        brains = self.attendees()
        attendees = dict([(b.UID, {'name': b.Title,
                     'organization': b.organization,
                     'review_state': b.review_state,
                     'type': b.Subject and b.Subject[0],
                     'badge_name': b.badge_name,
                     'gender': b.gender,
                     't_shirt_size': b.t_shirt_size,
                     'country': b.country,
                     'state': b.state,
                     'city': b.city,
                     'url': b.getURL(),
                     'json_url': '%s/json' % b.getURL(),
                     })
                    for b in brains])
        return attendees
    #
    @memoize
    def registration_info(self, uid):
        ''' Return registration info for a given uid '''
        return self.registrations_dict.get(uid, {})
    #
    @memoize
    def attendee_info(self, uid):
        ''' Return attendee info for a given uid '''
        return self.attendees_dict.get(uid, {})
    #
    @memoize
    def registrations_stats(self):
        stats = {}
        for state in ['pending', 'confirmed']:
            kw = {'review_state': state}
            stats[state] = {}
            stats[state]['registrations'] = len(self.registrations(**kw))
            stats[state]['attendees'] = len(self.attendees(**kw))
        return stats
    #
    @memoize
    def trainings(self):
        program_helper = self.program_helper
        kw = {'review_state': 'confirmed'}
        trainings = program_helper.trainings(**kw)
        return trainings
    #
    def speaker_name(self, speaker_uids):
        ''' Given a list os uids, we return a string with speakers names '''
        program_helper = self.program_helper
        speakers_dict = program_helper.speakers_dict
        results = [speaker for uid, speaker in speakers_dict.items()
                                           if uid in speaker_uids]
        return ', '.join([b['name'] for b in results])
