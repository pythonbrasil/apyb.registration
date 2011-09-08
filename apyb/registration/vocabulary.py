# -*- coding: utf-8 -*-

from sc.base.grokutils import registerSimpleVocabulary
from apyb.registration import MessageFactory as _

# registerSimpleVocabulary calls require the module global dictionary
# as the last parameter in order for grok to register its variables 
# in this module (normally it would be done silently 
# and implicitly by a call to grok.global_utils

registerSimpleVocabulary(
    "Gender", u"apyb.registration", 
    [('m',_(u'Male')),
     ('f',_(u'Female')),
    ],
    globals()
)

registerSimpleVocabulary(
    "TShirt", u"apyb.registration", 
    [
     ('S',_(u'Small')),
     ('M',_(u'Medium')),
     ('L',_(u'Large')),
     ('X',_(u'X-Large')),
    ],
    globals()
)

registerSimpleVocabulary(
    "Types", u"apyb.registration",
    [
     ('apyb',_(u'APyB Members')),
     ('student',_(u'Student')),
     ('individual',_(u'Individual')),
     ('government',_(u'Government')),
     ('group',_(u'Group/Corporate')),
     ('speaker',_(u'Speaker')),
     ('sponsor',_(u'Sponsor')),
    ],
    globals()
)

registerSimpleVocabulary(
    "PaymentServices", u"apyb.registration",
    [
     ('paypal',_(u'PayPal')),
     ('pagseguro',_(u'Pagseguro')),
    ],
    globals()
)