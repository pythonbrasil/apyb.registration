from five import grok
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
    
