# -*- coding:utf-8 -*-
from zope import schema
from zope.interface import alsoProvides

from plone.directives import form, dexterity
from plone.autoform.interfaces import IFormFieldProvider

from apyb.registration import MessageFactory as _


class IPaymentInformation(form.Schema):
    """
       Marker/Form interface for Payment Information
    """

    form.fieldset('payment',
            label=_(u"Payment Information"),
            fields=['service', 'paid', 'amount', ],
    )

    dexterity.read_permission(amount='zope2.View')
    dexterity.write_permission(service='cmf.ReviewPortalContent')
    service = schema.Choice(
        title=_(u'Payment service provider'),
        description=_(u'Which payment service provider was used?'),
        required=False,
        vocabulary="apyb.registration.paymentservices")

    dexterity.read_permission(paid='zope2.View')
    paid = schema.Bool(
        title=_(u'Is this paid?'),
        default=False,
        required=False,
        )

    dexterity.read_permission(amount='zope2.View')
    dexterity.write_permission(amount='cmf.ReviewPortalContent')
    amount = schema.Int(
        title=_(u'Amount paid?'),
        default=0,
        required=False,
    )


alsoProvides(IPaymentInformation, IFormFieldProvider)
