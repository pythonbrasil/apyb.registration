# -*- coding:utf-8 -*-
from five import grok
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from apyb.registration.registrations import IRegistrations
from random import choice


VALIDCHAR = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

class UsersView(grok.View):
    grok.context(IRegistrations)
    grok.require('cmf.ManagePortal')
    grok.name('report-users')
    
    def listRegistrations(self):
        ''' List registrations created here '''
        ct = getToolByName(self.context,'portal_catalog')
        results = ct.searchResults(portal_type='apyb.registration.registration')
        return [b.getObject() for b in results]
    
    def generatePass(self):
        senha = [choice(VALIDCHAR) for i in range(0,8)]
        return ''.join(senha)
    
    def render(self):
        data = []
        users = {}
        header = ['email','username','fullname','password','content']
        data.append(header)
        for item in self.listRegistrations():
            if not item.email in users:
                users[item.email] = {'data':[],'content':[]}
                tmpData = []
                tmpData.append(item.email)
                tmpData.append(item.email)
                tmpData.append(item.Title())
                tmpData.append(self.generatePass())
                users[item.email]['data'] = tmpData
            users[item.email]['content'].append(item.id)
        
        for v in users.values():
            line = v['data']
            line.extend(['|'.join(v['content']),])
            data.append(line)
        data = [','.join(line) for line in data]
        
        #self.request.response.setHeader('Content-Type', 'application/json')
        return '\n'.join(data)

class UpdateOwner(UsersView):
    grok.name('update-owner')
    
    def render(self):
        data = []
        mt = getToolByName(self.context,'portal_membership')
        for item in self.listRegistrations():
            email = item.email
            member = mt.getMemberById(email)
            if (not member):
                data.append('Member not found: %s' % email)
                continue
            if  email==item.getOwner().getUserName():
                data.append('Already fixed: %s' % email)
                continue
            objs = [item] + [i for i in item.objectValues()]
            for obj in objs:
                obj.creators = (email,)
                obj.changeOwnership(member.getUser())
            data.append('Ownership changed to %s' % email)
            
        return '\n'.join(data)