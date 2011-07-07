# -*- coding:utf-8 -*-
from random import choice
VALIDCHARS = 'abcdefghijklmnopqrstuvwxyz0123456789'
SIZE = 8

def generateId():
    ''' Generate an id '''
    uid = [choice(VALIDCHARS) for i in range(0,SIZE+1)] 
    return ''.join(uid)