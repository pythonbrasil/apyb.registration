# -*- coding:utf-8 -*-
from five import grok

from zope.event import notify
from zope.lifecycleevent import ObjectCreatedEvent

from plone.dexterity.utils import addContentToContainer
from plone.dexterity.utils import createContent
from plone.directives import form

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


from apyb.registration.training import ITrainingRegistration
from apyb.registration.registration import IRegistration

from apyb.registration import MessageFactory as _

class TrainingRegistration(form.SchemaAddForm):
    grok.context(IRegistration)
    grok.require('apyb.registration.AddTrainingRegistration')
    grok.name('registration-training')
    
    label = _(u"Training registrations")
    description = _(u"Register to pre-conference trainings")
    
    template = ViewPageTemplateFile('register_templates/new_training.pt')
    
    schema = ITrainingRegistration
    
    enable_form_tabbing = False
    member = None
    
    def __init__(self, context, request):
        super(TrainingRegistration, self).__init__(context, request)

    def update(self):        
        super(TrainingRegistration, self).update()
        self.request['disable_plone.leftcolumn']=1
        self.request['disable_plone.rightcolumn']=1

    def create(self, data):
        ''' Create registration '''
        registration = createContent('apyb.registration.training',
                                    checkConstraints=True, **data)

        return registration

    def add(self, object):
        registration = object
        context = self.context
        regObject = addContentToContainer(context,registration)
        regObject.paid = False
        regObject.service = None
        regObject.amount = 0.0
        event = ObjectCreatedEvent(regObject)
        notify(event)
        self.immediate_view = "%s/%s" % (context.absolute_url(), regObject.id)
        

