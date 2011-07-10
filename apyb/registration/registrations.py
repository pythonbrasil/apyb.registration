# -*- coding:utf-8 -*-
from five import grok

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

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
        self._ct = getToolByName(context,'portal_catalog')
    
    def registrations(self):
        ''' List registrations'''
        ct = self._ct
        results = ct.searchResults(portal_type='apyb.registration.registration',
                                   path=self._path)
        return results
    
    def attendees(self):
        ''' List attenddees'''
        ct = self._ct
        results = ct.searchResults(portal_type='apyb.registration.attendee',
                                   path=self._path)
        return results
    
    