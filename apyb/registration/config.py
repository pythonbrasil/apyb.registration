# -*- coding:utf-8 -*-

PRICES = {
          'apyb':16200,
          'student':18000,
          'individual':27000,
          'government':40000,
          'group':36000,
          'speaker':10000,
         }

GROUP_DISCOUNTS = {
    'student':[
        (3,0.25),
        (5,0.27),
        (7,0.32),
        (10,0.42),
        (100,0.42),
        ],
    
    'group':[
        (3,0.25),
        (5,0.27),
        (7,0.32),
        (10,0.42),
        (100,0.42),
        ]
}

REVIEW_STATE = {
    'confirmed':'Confirmado',
    'pending':'Pendente',
}