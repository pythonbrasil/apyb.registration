# -*- coding: utf-8 -*-
from five import grok
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm

class CountriesVocabulary(object):
    """Vocabulary factory for a list of countries
    """
    grok.implements(IVocabularyFactory)
    
    def __call__(self, context):
        paises = [('BR','Brasil'),('AR','Argentina'),]
        items = [SimpleTerm(k,k,v) for k,v in paises]
        return SimpleVocabulary(items)

grok.global_utility(CountriesVocabulary, name=u"apyb.registration.countries")

class GenderVocabulary(object):
    """Vocabulary factory for gender options
    """
    grok.implements(IVocabularyFactory)
    
    def __call__(self, context):
        paises = [('m','Male'),('f','Female'),]
        items = [SimpleTerm(k,k,v) for k,v in paises]
        return SimpleVocabulary(items)

grok.global_utility(GenderVocabulary, name=u"apyb.registration.gender")

class TShirtVocabulary(object):
    """Vocabulary factory for tshirt options
    """
    grok.implements(IVocabularyFactory)
    
    def __call__(self, context):
        paises = [('s','Small'),('m','Medium'),]
        items = [SimpleTerm(k,k,v) for k,v in paises]
        return SimpleVocabulary(items)

grok.global_utility(TShirtVocabulary, name=u"apyb.registration.tshirt")

class TypesVocabulary(object):
    """Vocabulary factory for types options
    """
    grok.implements(IVocabularyFactory)
    
    def __call__(self, context):
        paises = [('apyb','APyB Members'),('indiv','Individual'),]
        items = [SimpleTerm(k,k,v) for k,v in paises]
        return SimpleVocabulary(items)

grok.global_utility(TypesVocabulary, name=u"apyb.registration.types")

class PaymentServicesVocabulary(object):
    """Vocabulary factory for payment service providers
    """
    grok.implements(IVocabularyFactory)
    
    def __call__(self, context):
        services = [('paypal','PayPal'),('pagseguro','Pagseguro'),]
        items = [SimpleTerm(k,k,v) for k,v in services]
        return SimpleVocabulary(items)

grok.global_utility(TypesVocabulary, name=u"apyb.registration.paymentservices")

