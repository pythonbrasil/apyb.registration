# -*- coding:utf-8 -*-
from Acquisition import aq_inner
from Acquisition import aq_parent
from five import grok
from plone.directives import dexterity, form

from zope import schema

from plone.indexer import indexer

from zope.schema.interfaces import IVocabularyFactory
from zope.component import getMultiAdapter, queryUtility

from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds

from Products.CMFCore.interfaces import ISiteRoot

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
    form.omitted('training')
    training = schema.Choice(
        title=_(u'Training'),
        description=_(u'Select the Training'),
        required=True,
        vocabulary="apyb.papers.training",
    )
    #
    attendee = schema.Choice(
        title=_(u'Attendee'),
        description=_(u'Select the attendee'),
        required=True,
        vocabulary="apyb.registration.attendees",
    )


class TrainingRegistration(dexterity.Item):
    #
    grok.implements(ITrainingRegistration)
    #
    def _get_title(self):
        attendee_uid = self.attendee
        portal = getUtility(ISiteRoot)
        factory = queryUtility(IVocabularyFactory,
                               'apyb.registration.attendees')
        vocab = factory(portal)
        vocab_item = vocab.getTerm(attendee_uid)
        return vocab_item.title
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


@indexer(ITrainingRegistration)
def training(obj):
    return [obj.training, ]

grok.global_adapter(training, name="Subject")


class AddForm(dexterity.AddForm):
    grok.name('apyb.registration.training')
    grok.require('apyb.registration.AddTrainingRegistration')
    #
    def create(self, data):
        training = aq_parent(self.context)
        content = super(AddForm, self).create(data)
        content.id = str(data['attendee'])
        content.training = training.uid
        return content


class View(grok.View):
    grok.context(ITrainingRegistration)
    grok.require('zope2.View')
    #
    def update(self):
        super(View, self).update()
        context = aq_inner(self.context)
        self._path = '/'.join(context.getPhysicalPath())
        self.state = getMultiAdapter((context, self.request),
                                      name=u'plone_context_state')
        self.tools = getMultiAdapter((context, self.request),
                                      name=u'plone_tools')
        self.portal = getMultiAdapter((context, self.request),
                                      name=u'plone_portal_state')
        self._ct = self.tools.catalog()
        self.member = self.portal.member()
        self.roles_context = self.member.getRolesInContext(context)
        if not [r for r in self.roles_context
                        if r in ['Manager', 'Editor', 'Reviewer', ]]:
            self.request['disable_border'] = True
