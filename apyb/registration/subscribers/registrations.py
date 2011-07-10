# -*- coding:utf-8 -*-
import zope.event
from five import grok
from zope.lifecycleevent import IObjectAddedEvent
from zope.component import getUtility, getMultiAdapter

from Products.Five.utilities.marker import mark
from plone.app.contentrules.rule import Rule
from plone.app.contentrules.rule import get_assignments
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.engine.interfaces import IRuleAssignmentManager
from plone.contentrules.engine.assignments import RuleAssignment

from apyb.registration.registrations import IRegistrations
from apyb.registration import MessageFactory as _


@grok.subscribe(IRegistrations,IObjectAddedEvent)
def apply_rule(folder,event):
    ''' Apply content rule to execute a transition from new to pending
    '''
    name = 'rule-transition-registration'
    storage = getUtility(IRuleStorage)
    
    # Assignment
    assignable = IRuleAssignmentManager(folder, None)
    if assignable is None:
        return
      
    assignment = assignable.get(name, None)
    if assignment is None:
        assignment = assignable[name] = RuleAssignment(name) 
    assignment.enabled = True
    assignment.bubbles = False
    path = '/'.join(folder.getPhysicalPath())
    get_assignments(storage[name]).insert(path)