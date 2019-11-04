# -*- coding: utf-8 -*-
from __future__ import absolute_import
import cgi
import os
import re
import json
import webapp2
import jinja2
import traceback
import urllib, urllib2
import time
from datetime import date,datetime, timedelta

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import ndb
from google.appengine.ext import gql

import webapp2
from webapp2_extras import sessions

from models.models import Category
import sys
reload(sys)  
sys.setdefaultencoding('utf8')

#from webapp2_extras import jinja2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True,
)



class CategoryMain(webapp2.RequestHandler):
    def get(self):
        try:
        	#jinja = jinja2.get_jinja2(app=self.app)
        	#template = jinja.render_template("basic_table.html")
        	a = "hello world!!!"
        	sav = Category(
        		name = "politica",
        		keyword = [
                'beatriz argimón',
                'rodolfo nin novoa',
                'carmen beramendi',
                'rafael michelini',
                'jos\xe9 amor\xedn batlle',
                'fernando amado',
                'jos\xe9 mujica',
                'eleuterio fern\xe1ndez huidobro',
                'luc\xeda topolansky',
                'ministro',
                'nin novoa',
                'gobierno',
                'uruguay',
        		'frente amplio',
                'diputados',
                'legislador',
        		'senadora frenteamplista',
                'frenteamplista carmen beramendi',
                'frenteamplista rafael michelini',
                'nacionalista beatriz argimón',
                'frenteamplista',
                'nacionalista',
                'ministerio',
                'partidos',
                'partidos pol\xedticos',
                'partido colorado',
                'colorados',
                'partido nacional', 
                'partido independiente',
                'resultados electorales'
        		'senador',
                'campa\xf1a electoral',
                'senadora',
                'elecciones internas',
                'elecciones',
                'ley',
        		'nivel nacional',
                'interior',
                'ancap',
                'colectivo frenteamplista',
                'rep\xfablica',
                'marenales',
                'mln',
                'mpp',
        		'vamos uruguay',
                'territorio nacional',
                'actividad pol\xedtic']
        	)
        	sav.put()

            
        	template = JINJA_ENVIRONMENT.get_template('basic_table.html')
        	self.response.write(template.render(locals()))
        	#self.response.out.write(template.render(template_values))
        	#template = JINJA_ENVIRONMENT.get_template('/templates/mono2.html')
        except:
            error = traceback.format_exc()
            print error
            return True


class keywordExtract(webapp2.RequestHandler):
    def get(self, lista):
        """
        recorrer los stop words y si hay una coincidencia eliminarlo de la lista
        
        """
        lista = lista.split(".")
        lista2 = []
        print lista
        return True
        for i in lista:
            i = re.sub(r'[,.-:]','',i)
            i = re.sub(r'\d+', '', i)
            i.replace("<br>","")
            lista2.append(i.lower().decode('utf-8'))
        lista2 = set(lista2)
        lista2 = list(lista2)
        #lista2 = ["actualmente","acuerdo","adelante","ademas"]
        print lista2
        print "   "
        #return True
        try:
            with open("stop_words.txt", 'r') as f:
                for line in f:
                    line = line.split('\n')[0]
                    #print line.decode('utf-8')
                    if line.decode('utf-8') in lista2:
                        lista2.remove(line.decode('utf-8'))
                        print "remove --------------------"
                        print line.decode('utf-8')
        
        except:
            error = traceback.format_exc()
            print error

        print lista2
        return True

