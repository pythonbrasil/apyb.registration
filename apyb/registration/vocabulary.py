# -*- coding: utf-8 -*-
from Acquisition import aq_parent

from sc.base.grokutils import registerSimpleVocabulary

from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm

from Products.CMFCore.utils import getToolByName

from apyb.registration import MessageFactory as _

# registerSimpleVocabulary calls require the module global dictionary
# as the last parameter in order for grok to register its variables
# in this module (normally it would be done silently
# and implicitly by a call to grok.global_utils

registerSimpleVocabulary(
    "Gender", u"apyb.registration",
    [('m', _(u'Male')),
     ('f', _(u'Female')),
    ],
    globals(),
)

registerSimpleVocabulary(
    "TShirt", u"apyb.registration",
    [
     ('S', _(u'Small')),
     ('M', _(u'Medium')),
     ('L', _(u'Large')),
     ('X', _(u'X-Large')),
    ],
    globals(),
)

registerSimpleVocabulary(
    "Types", u"apyb.registration",
    [
     ('apyb', _(u'APyB Members')),
     ('student', _(u'Student')),
     ('individual', _(u'Individual')),
     ('government', _(u'Government')),
     ('group', _(u'Group/Corporate')),
     ('speaker', _(u'Speaker')),
     ('speaker_c', _(u'Speaker')),
     ('sponsor', _(u'Sponsor')),
     ('organizer', _(u'Organization')),
    ],
    globals(),
)

registerSimpleVocabulary(
    "PaymentServices", u"apyb.registration",
    [
     ('cash', _(u'Cash / At the conference')),
     ('paypal', _(u'PayPal')),
     ('pagseguro', _(u'Pagseguro')),
    ],
    globals(),
)


def attendeesVocabulary(context):
    """Vocabulary factory for attendees
    """
    ct = getToolByName(context, 'portal_catalog')
    dictSearch = {'portal_type': 'apyb.registration.attendee',
                  'sort_on': 'sortable_title',
                  'review_state': 'confirmed'}
    attendees = ct.searchResults(**dictSearch)
    attendees = [SimpleTerm(b.UID, b.UID, b.Title) for b in attendees]
    return SimpleVocabulary(attendees)

registerSimpleVocabulary(
    "Attendees", u"apyb.registration",
    attendeesVocabulary,
    globals(),
)


def attendeesRegistrationVocabulary(context):
    """Vocabulary factory for attendees
    """
    ct = getToolByName(context, 'portal_catalog')
    if context.portal_type == 'apyb.registration.training':
        context = aq_parent(context)
    path = '/'.join(context.getPhysicalPath())
    dictSearch = {'portal_type': 'apyb.registration.attendee',
                  'sort_on': 'sortable_title',
                  'path': path,
                  'review_state': 'confirmed'}
    attendees = ct.searchResults(**dictSearch)
    attendees = [SimpleTerm(b.UID, b.UID, b.Title) for b in attendees]
    return SimpleVocabulary(attendees)

registerSimpleVocabulary(
    "Attendees_registration", u"apyb.registration",
    attendeesRegistrationVocabulary,
    globals(),
)


def trainingsVocabulary(context):
    """Vocabulary factory for trainings
    """
    ct = getToolByName(context, 'portal_catalog')
    dictSearch = {'portal_type': 'apyb.papers.training',
                  'sort_on': 'sortable_title',
                  'review_state': 'confirmed'}
    trainings = ct.searchResults(**dictSearch)
    trainings = [SimpleTerm(b.UID, b.UID, b.Title) for b in trainings]
    return SimpleVocabulary(trainings)


registerSimpleVocabulary(
    "Trainings", u"apyb.registration",
    trainingsVocabulary,
    globals(),
)
