# -*- coding: utf-8 -*-
from five import grok
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm

from apyb.registration import MessageFactory as _

global_utility = grok.global_utility

#FIXME: Refactor this function into a separate product:
def registerSimpleVocabulary(vocabulary_name, package_path, items):
    """
        Register a sequence of duples as a SimpleVocabulary, 
        with the given vocabulary_name at package_path
    """
    #metaclass needed due to grok's black magic with its
    # function calls that change class behaviors. 
    # otherwise a call to "type" would do rather than
    # needing this metaclass and the inlining of Vocabulary bellow
    
    def metaAutoSimpleVocabulary(name, bases, dct):
        dct["__doc__"] = "Vocabulary factory for %s options" % vocabulary_name
        return type(vocabulary_name + "Vocabulary", (object,), dct)
        
    class Vocabulary:
        __metaclass__ = metaAutoSimpleVocabulary
        grok.implements(IVocabularyFactory)
        
        def __call__(self, context):
            vocab_items = [SimpleTerm(k,k,v) for k,v in items]
            return SimpleVocabulary(vocab_items)
    # More grok black magick - the grok.global_utility "must be called from module level"
    # GROK developers: this ain't programing. One of the first predicates of a "function"
    # is that it does not change any state where it is called.
    # FIXME: Create some white anti-grok-black-magic to get the following working:
    #grok.global_utility(Vocabulary, name=package_path + "." + unicode(vocabulary_name, "utf-8").lower())
    return (Vocabulary, package_path + "." + unicode(vocabulary_name, "utf-8").lower())

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