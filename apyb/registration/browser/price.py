# -*- coding:utf-8 -*-
import json
from five import grok

from Acquisition import aq_inner

from apyb.registration.registrations import IRegistrations

from apyb.registration.config import PRICES,GROUP_DISCOUNTS

class PriceView(grok.View):
    grok.context(IRegistrations)
    grok.require('zope2.View')
    grok.name('reg-price')
    
    def price(self,registration_type,qty):
        base_price = PRICES[registration_type]
        grp_discount = GROUP_DISCOUNTS.get(registration_type,[])
        discount = 0.0
        if grp_discount and qty >2:
            for line in grp_discount:
                if line[0] > qty:
                    discount = line[1]
        price = base_price * qty * (1-discount)
        return price
    
    def fmtPrice(self,price):
        return ('R$%.2f' % (price/100.0)).replace('.',',')
    
    def render(self):
        return ''

class PriceJsonView(PriceView):
    grok.name('reg-price.json')
    
    def render(self):
        request = self.request
        registration_type = request.get('type','individual')
        qty = int(request.get('qty',1))
        context = aq_inner(self.context)
        data = {'price':0.0,'fmtPrice':'R$0,00'}
        data['price'] = self.price(registration_type,qty)
        data['fmtPrice'] = self.fmtPrice(data['price'])
        
        self.request.response.setHeader('Content-Type', 'application/json')
        
        return json.dumps(data)