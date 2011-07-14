from zope.interface import alsoProvides
from zope.component import adapts
from zope import schema
from plone.directives import form
from plone.dexterity.interfaces import IDexterityContent
from plone.autoform.interfaces import IFormFieldProvider
from apyb.registration import MessageFactory as _

class IOptInInformation(form.Schema):
   """
      Marker/Form interface for OptIn information
   """
   conference = schema.Bool(
       title=_(u'Accept to be contacted by conference organizers'),
       default=True,
       required=False,
       )

   partners = schema.Bool(
       title=_(u'Accept to be contacted by conference partners'),
       default=True,
       required=False,
       )
   

alsoProvides(IOptInInformation,IFormFieldProvider)
