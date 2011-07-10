# -*- coding:utf-8 -*-
import zope.event
from five import grok
from Products.CMFCore.interfaces import IActionSucceededEvent

from Products.CMFCore.utils import getToolByName
from zope.component import getUtility, getMultiAdapter

from apyb.registration.registration import IRegistration
from apyb.registration import MessageFactory as _

@grok.subscribe(IRegistration, IActionSucceededEvent)
def update_attendees(folder,event):
    ''' Set correct state to attendees under this object
    '''
    wt = getToolByName(folder,'portal_workflow')
    objects = folder.objectValues()
    # Confirm or cancel
    if event.action in ['confirm','cancel',]:
        transition = event.action
    else:
        return 
    for obj in objects:
        wt.doActionFor(obj,transition)
    
    