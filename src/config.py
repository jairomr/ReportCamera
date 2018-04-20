#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
"""
Configuração da pasta do sistema report
Requer python 2.7
"""
path = '{}/'.format(os.getcwd()) #"C:/camerasRelatorio/"
debug = 1
"""
Cofiguração de envio de email
"""
emails = [
    'nxgame2009@gmail.com'
    ]
subject = 'Tanguro - Status camera'
smtp_server = 'smtp.gmail.com'
smtp_user = 'email@gmail.com'
smtp_pass = 'senha'
strFrom = 'email@gmail.com'


if debug == 1:
    print(path)
    print('Debuf esta ativo')
    emails = ['nxgame2009@gmail.com']
    subject = 'Teste do Script Configuraçãodo Grafico 7 dias'

"""
Conteudo do Report
"""
imgs = [
    {'img':'gf1.jpg','cid':'image1'},
]

"""
Ftp config
"""
ftpGetFiles = [
    {
       'host': 'host',
       'user': 'user',
       'pass': 'senha',
       'port': '21',
       'path': '/public_html'
    }
]

"""
Configuração de tentativas de conexão
"""
waitingTime = 10#Time for next second attempt
numberAttempts = 15#Number of attempts

if debug == 1:
    waitingTime = 1 #Time for next second attempt
    numberAttempts = 2 #Number of attempts



