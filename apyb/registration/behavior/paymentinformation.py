from zope.interface import alsoProvides
from zope.component import adapts
from zope import schema
from plone.directives import form, dexterity
from plone.dexterity.interfaces import IDexterityContent
from plone.autoform.interfaces import IFormFieldProvider
from apyb.registration import MessageFactory as _

class IPaymentInformation(form.Schema):
   """
      Marker/Form interface for Payment Information
   """
   dexterity.read_permission(service='cmf.ReviewPortalContent')
   dexterity.write_permission(service='cmf.ReviewPortalContent')
   service = schema.Choice(
       title=_(u'Payment service provider'),
       description=_(u'Which payment service provider was used?'),
       required=False,
       vocabulary="apyb.registration.paymentservices"
       )
   
   paid = schema.Bool(
       title=u'Is this paid?',
       default=False,
       required=False,
       )

   dexterity.read_permission(amount='cmf.ReviewPortalContent')
   dexterity.write_permission(amount='cmf.ReviewPortalContent')
   amount = schema.Int(
       title=u'Amount paid?',
       default=0,
       required=False,
   )
   

alsoProvides(IPaymentInformation,IFormFieldProvider)

