# -*- coding: utf-8 -*-
from __future__ import absolute_import
import time
from datetime import date,datetime, timedelta
from google.appengine.ext import webapp
import jinja2
import traceback
import os
import webapp2

from models.models import News3, NewsSelect2, News
from google.appengine.ext.webapp import template

import sys
reload(sys)  
sys.setdefaultencoding('utf8')

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True,
)



class DeleteNewsSelect(webapp2.RequestHandler):
    '''  '''
    def get(self):
        hoy = date.today()
        f = NewsSelect2.query(
            NewsSelect2.date == hoy,
        ).fetch()
        for i in f:
            i.key.delete()

        clima = Clima()
        cli = clima.get()
        
        return webapp2.redirect('/')
        template = JINJA_ENVIRONMENT.get_template('/templates/index.html')
        self.response.write(template.render(locals()))


class DeleteMontevideoCom(webapp2.RequestHandler):
    '''  '''
    def get(self):
        hoy = date.today()
        f = News3.query(
            News3.date == hoy,
            News3.news_from.IN([
                "montevideo_com",
                
            ])
        ).fetch()
        for i in f:
            i.key.delete()

        template_values = {
            'data': f,
            'fecha': hoy,
            #'data3': data3,
        }
        template = JINJA_ENVIRONMENT.get_template('/templates/index.html')
        self.response.write(template.render(template_values))


class DeleteCientoOchenta(webapp2.RequestHandler):
    '''  '''
    def get(self):
        hoy = date.today()
        f = News3.query(
            News3.date == hoy,
            News3.news_from.IN([
                "ciento_ochenta",
            ])
        ).fetch()
        for i in f:
            i.key.delete()

        template_values = {
            'data': f,
            'fecha': hoy,
            #'data3': data3,
        }
        template = JINJA_ENVIRONMENT.get_template('/templates/index.html')
        self.response.write(template.render(template_values))


class DeleteElPais(webapp2.RequestHandler):
    '''  '''
    def get(self):
        hoy = date.today()
        f = News3.query(
            News3.date == hoy,
            News3.news_from.IN([
                "el_pais",
            ])
        ).fetch()
        for i in f:
            i.key.delete()

        template_values = {
            'data': f,
            'fecha': hoy,
            #'data3': data3,
        }
        return webapp2.redirect('/')
        template = JINJA_ENVIRONMENT.get_template('/templates/index.html')
        self.response.write(template.render(template_values))


# class DeleteHoroscopo(webapp2.RequestHandler):
#     '''  '''
#     def get(self):
#         hoy = date.today()
#         f = Horoscopos.query(
#             Horoscopos.date == hoy,
#         ).fetch()
#         for i in f:
#             i.key.delete()

#         template_values = {
#             'data': f,
#             'fecha': hoy,
#             #'data3': data3,
#         }
#         template = JINJA_ENVIRONMENT.get_template('/templates/index.html')
#         self.response.write(template.render(template_values))


class DeleteUyPress(webapp2.RequestHandler):
    '''  '''
    def get(self):
        hoy = date.today()
        f = News3.query(
            News3.date == hoy,
            News3.news_from.IN([
                "uy_press",
            ])
        ).fetch()
        for i in f:
            i.key.delete()

        template_values = {
            'data': f,
            'fecha': hoy,
            #'data3': data3,
        }
        template = JINJA_ENVIRONMENT.get_template('/templates/index.html')
        self.response.write(template.render(template_values))


class DeleteLaDiaria(webapp2.RequestHandler):
    '''  '''
    def get(self):
        hoy = date.today()
        f = News3.query(
            News3.date == hoy,
            News3.news_from.IN([
                "la_diaria",
            ])
        ).fetch()
        for i in f:
            i.key.delete()

        template_values = {
            'data': f,
            'fecha': hoy,
            #'data3': data3,
        }
        return webapp2.redirect('/')
        template = JINJA_ENVIRONMENT.get_template('/templates/index.html')
        self.response.write(template.render(template_values))


class DeleteElObservador(webapp2.RequestHandler):
    '''  '''
    def get(self):
        hoy = date.today()
        f = News3.query(
            News3.date == hoy,
            News3.news_from.IN([
                "el_observador",
            ])
        ).fetch()
        for i in f:
            i.key.delete()

        template_values = {
            'data': f,
            'fecha': hoy,
            #'data3': data3,
        }
        template = JINJA_ENVIRONMENT.get_template('/templates/index.html')
        self.response.write(template.render(template_values))


class DeleteSubrayado(webapp2.RequestHandler):
    '''  '''
    def get(self):
        hoy = date.today()
        f = News3.query(
            News3.date == hoy,
            News3.news_from.IN([
                "subrayado",
            ])
        ).fetch()
        for i in f:
            i.key.delete()

        template_values = {
            'data': f,
            'fecha': hoy,
            #'data3': data3,
        }
        template = JINJA_ENVIRONMENT.get_template('/templates/index.html')
        self.response.write(template.render(template_values))


class DeleteNews(webapp2.RequestHandler):
    '''  '''
    def get(self):
        
        f = News2.query().fetch()
        for i in f:
            i.key.delete()

        template_values = {
            'data': f,
            'fecha': hoy,
            #'data3': data3,
        }
        template = JINJA_ENVIRONMENT.get_template('/templates/mono2.html')
        self.response.write(template.render(template_values))