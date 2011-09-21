# -*- coding:utf-8 -*-
from Acquisition import aq_inner
from Acquisition import aq_parent

from five import grok
from plone.directives import dexterity, form

from zope import schema

from zope.schema.interfaces import IVocabularyFactory
from zope.component import getMultiAdapter, queryUtility

from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds

from plone.indexer import indexer

from apyb.registration import MessageFactory as _


class IAttendee(form.Schema):
    """
    An attenddee at a conference
    """
    form.omitted('uid')
    uid = schema.Int(
        title=_(u"uid"),
        required=False,
        )
    #
    registration_type = schema.Choice(
        title=_(u'Type'),
        description=_(u'Select the category of your registration'),
        required=False,
        vocabulary="apyb.registration.types",
    )
    #
    fullname = schema.TextLine(
        title=_(u'Fullname'),
        description=_(u'Please inform your fullname'),
        required=True,
    )
    #
    badge_name = schema.TextLine(
        title=_(u'Badge name'),
        description=_(u'Please inform the name that will appear on your badge'
                      u' -- Leave it blank to use your fullname in the badge'),
        required=False,
        missing_value=u'',
    )
    #
    organization = schema.TextLine(
        title=_(u'Organization'),
        description=_(u'Please inform the name of the organization you'
                      u'will represent'),
        required=False,
        missing_value=u'',
    )
    #
    gender = schema.Choice(
        title=_(u'Gender'),
        required=True,
        vocabulary="apyb.registration.gender",
    )
    #
    t_shirt_size = schema.Choice(
        title=_(u'T-Shirt Size'),
        required=True,
        vocabulary="apyb.registration.tshirt",
    )
    #
    form.omitted('uid')
    trainings = schema.List(
        title=_(u'Trainings'),
        description=_(u'Select trainings'),
        default=[],
        value_type=schema.Choice(title=_(u"Training"),
                                 vocabulary='apyb.registration.trainings'),
        required=False,
    )


class Attendee(dexterity.Item):
    grok.implements(IAttendee)
    #
    def _get_title(self):
        return self.fullname
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


@indexer(IAttendee)
def registration_type(obj):
    return [obj.registration_type, ]
grok.global_adapter(registration_type, name="Subject")


class View(grok.View):
    grok.context(IAttendee)
    grok.require('zope2.View')
    #
    def update(self):
        super(View, self).update()
        context = aq_inner(self.context)
        registration = aq_parent(context)
        registrations = aq_parent(registration)
        self.registration_type = self.context.registration_type
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
                                   'apyb.registration.types')
        self.voc = voc_factory(context)
        self.roles_context = self.member.getRolesInContext(context)
        if not [r for r in self.roles_context
                        if r in ['Manager', 'Editor', 'Reviewer', ]]:
            self.request['disable_border'] = True
    #
    @property
    def trainings(self):
        helper = self.helper
        program_helper = helper.program_helper
        trainings_dict = program_helper.trainings_dict
        return trainings_dict
    #
    def registered_trainings(self):
        registered = self.context.trainings
        trainings = self.trainings
        data = []
        for uid, training in trainings.items():
            if not (uid in registered):
                continue
            data.append(training)
        return data
    #
    def available_trainings(self):
        trainings = self.trainings
        data = []
        for uid, training in trainings.items():
            state = training.get('review_state','')
            seats = training.get('seats',0)
            if not (state == 'confirmed' and seats):
                continue
            data.append(training)
        return data
    #
    @property
    def allow_training_registering(self):
        if not 'Owner' in self.roles_context:
            return False
        state = self.state
        review_state = state.workflow_state()
        return review_state == 'confirmed'
    #
    @property
    def fmt_registration_type(self):
        registration_type = self.registration_type
        if registration_type:
            term = self.voc.getTerm(registration_type)
            return term.title

class RegisterView(View):
    grok.context(IAttendee)
    grok.require('cmf.ModifyPortalContent')
    grok.name('register_trainings')

    template = None

    def render(self):
        trainings_uid = self.request.form.get('trainings_uid',[])
        if isinstance(trainings_uid,str):
            trainings_uid = [trainings_uid,]
        trainings_uid = [int(uid) for uid in trainings_uid]
        self.context.trainings = trainings_uid
        self.context.reindexObject(idxs=['trainings',])
        return self.request.response.redirect(self.context.absolute_url())
