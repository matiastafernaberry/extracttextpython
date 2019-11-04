# -*- coding: utf-8 -*-
from __future__ import absolute_import
import time
from datetime import date,datetime, timedelta
from google.appengine.ext import webapp
import jinja2
import traceback
import os
import webapp2

from views.charrua.subrayado import Subrayado
from views.charrua.elpais import Elpais
from views.charrua.elobservador import ElObservador
from views.charrua.montevideo_com import MontevideoCom
from views.charrua.ciento_ochenta import CientoOchenta
from views.charrua.la_diaria import LaDiaria
from views.charrua.uy_press import UyPress, UypressPolitica, UypressEconomia, UypressDeportes
from views.charrua.lr21 import Lr21
from views.charrua.la_republica import LaRepublica

import sys
reload(sys)  
sys.setdefaultencoding('utf8')

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True,
)

class CronElpais(webapp2.RequestHandler):
    def get(self):
        try:
            ep = Elpais()
            elpais = ep.get()

            template = JINJA_ENVIRONMENT.get_template('/templates/mono2.html')
            self.response.write(template.render(locals()))
        except:
            error = traceback.format_exc()
            template_values = {
                'error': error,
                
            }
            template = JINJA_ENVIRONMENT.get_template('/templates/mono2.html')
            self.response.write(template.render(locals()))


class CronUyPress(webapp2.RequestHandler):
    def get(self):
        try:
            try: 
                u = UyPress()
                u = u.get()
            except: pass
            try: 
                e = UypressPolitica()
                e = e.get()
            except: pass

            try: 
                e = UypressEconomia()
                e = e.get()
            except: pass

            try: 
                e = UypressDeportes()
                e = e.get()
            except: pass

            template = JINJA_ENVIRONMENT.get_template('/templates/mono2.html')
            self.response.write(template.render(locals()))
        except:
            error = traceback.format_exc()
            template_values = {
                'error': error,
                
            }
            template = JINJA_ENVIRONMENT.get_template('/templates/mono2.html')
            self.response.write(template.render(locals()))


class CronMontevideocom(webapp2.RequestHandler):
    def get(self):
        try:
            u = MontevideoCom()
            u = u.get()

            template = JINJA_ENVIRONMENT.get_template('/templates/mono2.html')
            self.response.write(template.render(locals()))
        except:
            error = traceback.format_exc()
            template_values = {
                'error': error,
                
            }
            template = JINJA_ENVIRONMENT.get_template('/templates/mono2.html')
            self.response.write(template.render(locals()))


class CronLaDiaria(webapp2.RequestHandler):
    def get(self):
        try:
            u = LaDiaria()
            u = u.get()

            return webapp2.redirect('/')
            template = JINJA_ENVIRONMENT.get_template('/templates/mono2.html')
            self.response.write(template.render(locals()))
        except:
            error = traceback.format_exc()
            template_values = {
                'error': error,
                
            }
            template = JINJA_ENVIRONMENT.get_template('/templates/mono2.html')
            self.response.write(template.render(locals()))


class CronCientoochenta(webapp2.RequestHandler):
    def get(self):
        try:
            u = CientoOchenta()
            u = u.get()

            template = JINJA_ENVIRONMENT.get_template('/templates/mono2.html')
            self.response.write(template.render(locals()))
        except:
            error = traceback.format_exc()
            template_values = {
                'error': error,
                
            }
            template = JINJA_ENVIRONMENT.get_template('/templates/mono2.html')
            self.response.write(template.render(locals()))


class CronElObservador(webapp2.RequestHandler):
    def get(self):
        try:
            u = ElObservador()
            u = u.get()

            template = JINJA_ENVIRONMENT.get_template('/templates/mono2.html')
            self.response.write(template.render(locals()))
        except:
            error = traceback.format_exc()
            template_values = {
                'error': error,
                
            }
            template = JINJA_ENVIRONMENT.get_template('/templates/mono2.html')
            self.response.write(template.render(locals()))


class CronLr21(webapp2.RequestHandler):
    def get(self):
        try:
            u = Lr21()
            u = u.get()

            template = JINJA_ENVIRONMENT.get_template('/templates/mono2.html')
            self.response.write(template.render(locals()))
        except:
            error = traceback.format_exc()
            template_values = {
                'error': error,
                
            }
            template = JINJA_ENVIRONMENT.get_template('/templates/mono2.html')
            self.response.write(template.render(locals()))



class CronHoroscopo(webapp2.RequestHandler):
    def get(self):
        try:
            
            #o = Horoscopo()
            #o = o.post()

            template = JINJA_ENVIRONMENT.get_template('/templates/mono2.html')
            self.response.write(template.render(locals()))
        except:
            error = traceback.format_exc()
            template_values = {
                'error': error,
                
            }
            template = JINJA_ENVIRONMENT.get_template('/templates/mono2.html')
            self.response.write(template.render(locals()))


class CronSubrayado(webapp2.RequestHandler):
    def get(self):
        try:
            o = Subrayado()
            o = o.get()
        except:
            error = traceback.format_exc()
            print error


class CronElpais(webapp2.RequestHandler):
    def get(self):
        try:
            print "el pais"
            ep = Elpais()
            elpais = ep.get()
            self.redirect("/")
        except:
            error = traceback.format_exc()
            print error
            template_values = {
                'error': error,
            }
            template = JINJA_ENVIRONMENT.get_template('/templates/mono2.html')
            self.response.write(template.render(locals()))


class Cron(webapp2.RequestHandler):
    def get(self):
        try:
            ep = Elpais()
            elpais = ep.get()

            u = Lr21()
            u = u.get()

            u = CientoOchenta()
            u = u.get()

            u = MontevideoCom()
            u = u.get()

            u = UyPress()
            u = u.get()

            o = ElObservador()
            o = o.get()

            template = JINJA_ENVIRONMENT.get_template('/templates/mono2.html')
            self.response.write(template.render(locals()))
        except:
            error = traceback.format_exc()
            template_values = {
                'error': error,
                
            }
            template = JINJA_ENVIRONMENT.get_template('/templates/mono2.html')
            self.response.write(template.render(locals()))