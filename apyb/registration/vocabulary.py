# -*- coding: utf-8 -*-
from five import grok
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm

from apyb.registration import MessageFactory as _

class GenderVocabulary(object):
    """Vocabulary factory for gender options
    """
    grok.implements(IVocabularyFactory)
    
    def __call__(self, context):
        gender = [('m',_(u'Male')),
                  ('f',_(u'Female')),
                 ]
        items = [SimpleTerm(k,k,v) for k,v in gender]
        return SimpleVocabulary(items)

grok.global_utility(GenderVocabulary, name=u"apyb.registration.gender")

class TShirtVocabulary(object):
    """Vocabulary factory for tshirt options
    """
    grok.implements(IVocabularyFactory)
    
    def __call__(self, context):
        sizes = [
                 ('S',_(u'Small')),
                 ('M',_(u'Medium')),
                 ('L',_(u'Large')),
                 ('X',_(u'X-Large')),
                ]
        items = [SimpleTerm(k,k,v) for k,v in sizes]
        return SimpleVocabulary(items)

grok.global_utility(TShirtVocabulary, name=u"apyb.registration.tshirt")

class TypesVocabulary(object):
    """Vocabulary factory for types options
    """
    grok.implements(IVocabularyFactory)
    
    def __call__(self, context):
        types = [
                 ('apyb',_(u'APyB Members')),
                 ('student',_(u'Student')),
                 ('individual',_(u'Individual')),
                 ('government',_(u'Government')),
                 ('group',_(u'Group/Corporate')),
                ]
        items = [SimpleTerm(k,k,v) for k,v in types]
        return SimpleVocabulary(items)

grok.global_utility(TypesVocabulary, name=u"apyb.registration.types")

class PaymentServicesVocabulary(object):
    """Vocabulary factory for payment service providers
    """
    grok.implements(IVocabularyFactory)
    
    def __call__(self, context):
        services = [
                    ('paypal',_(u'PayPal')),
                    ('pagseguro',_(u'Pagseguro')),
                   ]
        items = [SimpleTerm(k,k,v) for k,v in services]
        return SimpleVocabulary(items)

grok.global_utility(TypesVocabulary, name=u"apyb.registration.paymentservices")

