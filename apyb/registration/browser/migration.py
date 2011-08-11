# -*- coding:utf-8 -*-
from five import grok
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from apyb.registration.registrations import IRegistrations
from random import choice


VALIDCHAR = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

TEMPLATE = """%s,
Você está recebendo esta mensagem para informá-lo que foi criada uma
conta de acesso ao site da PythonBrasil[7] para você.
Para acessar o site, use os dados a seguir:
    
    Endereço: http://www.pythonbrasil.org.br/login_form
    E-mail: %s
    Senha: %s
    
Você deverá alterar esta senha em seu primeiro acesso.

Utilize estes dados para se inscrever na PythonBrasil[7], verificar o estado 
de uma inscrição já enviada e submeter propostas de palestras!

Esperamos que você esteja presente nesta edição da PythonBrasil, o encontro 
da comunidade Python brasileira.

Associação Python Brasil - APyB
"""

class ResetPasswdView(grok.View):
    grok.context(IRegistrations)
    grok.require('cmf.ManagePortal')
    grok.name('reset-passwords')
    
    users = []
    
    def generatePass(self):
        senha = [choice(VALIDCHAR) for i in range(0,8)]
        return ''.join(senha)
    
    def sendEmail(self,member,passwd):
        ''' Send an email telling the user he has a new passwd'''
        subject = 'PythonBrasil[7]: Dados de acesso ao site'
        body = TEMPLATE % (member.getProperty('fullname',''),
                          member.getUserName(),
                          passwd,
                          )
        self.mail.send(body,
                       member.getUserName(),
                       self.mail_from,
                       subject=subject, 
                       charset='utf-8')
        
    
    def render(self):
        data = []
        self.plone_utils = getToolByName(self.context, 'plone_utils')
        self.urltool = getToolByName(self.context, 'portal_url')
        portal = self.urltool.getPortalObject()
        self.mail = getToolByName(self.context,'MailHost')
        self.mail_from = portal.getProperty('email_from_address')
        mt = getToolByName(self.context,'portal_membership')
        if not self.users:
            # we expect a list of emails separated by |
            users = self.request.get('users','').split('|')
        else:
            users = self.users
        for item in users:
            member = mt.getMemberById(item)
            if not member:
                continue
            passwd = self.generatePass()
            member.setSecurityProfile(password=passwd)
            member.setMemberProperties(dict(login_time='2000/01/01',must_change_password=1,))
            self.sendEmail(member,passwd)
        return '\n'.join(users)

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
    
    def sanitize_email(self,email):
        return '%s@%s' % ((email.split('@')[0]).split('+')[0],email.split('@')[1])
    
    def createMember(self,item):
        mt = self.mt
        registration = getToolByName(self.context, 'portal_registration')
        email = self.sanitize_email(item.email)
        try:
            registration.addMember(email, 
                                   'pythonbrasil_2011',
                                   ('Member',),
                                   properties={'username': email,
                                               'email': item.email,
                                               'location':item.country,
                                               'must_change_password':True,
                                               'fullname':item.Title()})
        except:
            # something went wrong
            pass
        return mt.getMemberById(email)
    
    def render(self):
        data = []
        mt = getToolByName(self.context,'portal_membership')
        self.mt = mt
        for item in self.listRegistrations():
            email = self.sanitize_email(item.email)
            member = mt.getMemberById(email)
            if (not member):
                data.append('Member not found: %s' % email)
                member = self.createMember(item)
            if  email==item.getOwner().getUserName():
                data.append('Already fixed: %s' % email)
                continue
            objs = [item] + [i for i in item.objectValues()]
            for obj in objs:
                obj.creators = (email,)
                obj.changeOwnership(member.getUser())
            data.append('Ownership changed to %s' % email)
            
        return '\n'.join(data)