# -*- coding:utf-8 -*-
from random import choice
VALIDCHARS = 'abcdefghijklmnopqrstuvwxyz0123456789'
SIZE = 8

def fmtPrice(price):
    ''' Format a value as price'''
    price = str(price).strip()
    if price:
        if price == '0':
            price = '0000'
        return 'R$ %s,%s' % (price[:-2],price[-2:])
    else:
        return '-'
def generateId():
    ''' Generate an id '''
    uid = [choice(VALIDCHARS) for i in range(0,SIZE+1)] 
    return ''.join(uid)