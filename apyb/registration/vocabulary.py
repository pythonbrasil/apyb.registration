# -*- coding: utf-8 -*-
from five import grok

from apyb.registration import MessageFactory as _

from sc.base.grokutils import registerSimpleVocabulary

global_utility = grok.global_utility

voc, name = registerSimpleVocabulary(
    "Gender", u"apyb.registration", 
    [('m',_(u'Male')),
     ('f',_(u'Female')),
    ]
)
global_utility(voc, name=name)

voc, name = registerSimpleVocabulary(
    "TShirt", u"apyb.registration", 
    [
     ('S',_(u'Small')),
     ('M',_(u'Medium')),
     ('L',_(u'Large')),
     ('X',_(u'X-Large')),
    ]
)
global_utility(voc, name=name)


voc, name = registerSimpleVocabulary(
    "Types", u"apyb.registration",
    [
     ('apyb',_(u'APyB Members')),
     ('student',_(u'Student')),
     ('individual',_(u'Individual')),
     ('government',_(u'Government')),
     ('group',_(u'Group/Corporate')),
    ]
)
global_utility(voc, name=name)

voc, name = registerSimpleVocabulary(
    "PaymentServices", u"apyb.registration",
    [
     ('paypal',_(u'PayPal')),
     ('pagseguro',_(u'Pagseguro')),
    ]
)
global_utility(voc, name=name)