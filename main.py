# -*- coding: utf-8 -*-
from __future__ import absolute_import
import sys
import cgi
import os
import re
import json
import webapp2
import jinja2
import traceback
import urllib, urllib2
import time
import logging
from datetime import date,datetime, timedelta

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import ndb
from google.appengine.ext import gql

import webapp2
from webapp2_extras import sessions

from bs4 import BeautifulSoup

from views.classification.testclassifier import TestClassifier

from views.delete_news.delete import *
from views.cron.cron import *

from views.htmltotext.htmltotext3 import HtmlToTextMain as HtmlToTextMain3
from views.htmltotext.htmltotext4 import HtmlToTextMain as HtmlToTextMain2

from views.category.category import CategoryMain
from views.otrosine.otrosine import Otrosine
#from views.charrua.gsearch import Gsearch
import sys
reload(sys)  
sys.setdefaultencoding('utf8')

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True,
)


def handle_404(request, response, exception):
    template = JINJA_ENVIRONMENT.get_template('/templates/404.html')
    request.response.write(template.render(locals()))
def handle_500(request, response, exception):
    logging.exception(exception)
    response.write('A server error occurred!')
    response.set_status(500)
        


class Google(webapp2.RequestHandler):
    def get(self):
        
        template = JINJA_ENVIRONMENT.get_template('/templates/googlea6bed3b812c0e8c8.html')
        self.response.write(template.render(locals()))


class HtmlToTextView(webapp2.RequestHandler):
    def get(self):
        try:
            #print "hello"
            c = HtmlToTextMain2()
            page = "https://www.elpais.com.uy/sabado-show/pasarela-inclusiva.html"
            o = c.main(page)

            template_values = {
                'data': o,
                
            }
            template = JINJA_ENVIRONMENT.get_template('/templates/profile2.html')
            self.response.write(template.render(template_values))
        except:
            error = traceback.format_exc()
            template_values = {
                'error': error,
            }
            template = JINJA_ENVIRONMENT.get_template('/templates/mono2.html')
            self.response.write(template.render(template_values))


class Robots(webapp2.RequestHandler):
    def get(self):
        try:
            template = JINJA_ENVIRONMENT.get_template('/templates/robots.txt')
            self.response.write(template.render(locals()))
        except:
            error = traceback.format_exc()
            template_values = {
                'error': error,
            }
            template = JINJA_ENVIRONMENT.get_template('/templates/index.html')
            self.response.write(template.render(template_values))


class Sitemap(webapp2.RequestHandler):
    def get(self):
        try:
            template = JINJA_ENVIRONMENT.get_template('/templates/sitemap.xml')
            self.response.write(template.render(locals()))
        except:
            error = traceback.format_exc()
            template_values = {
                'error': error,
            }
            template = JINJA_ENVIRONMENT.get_template('/templates/index.html')
            self.response.write(template.render(template_values))


class Comentarios(webapp2.RequestHandler):
    def get(self):
        try:
            template_values = {
                'empty': "hello",
            }

            template = JINJA_ENVIRONMENT.get_template('/templates/comentarios.html')
            self.response.write(template.render(template_values))
        except:
            error = traceback.format_exc()
            template_values = {
                'error': error,
            }
            template = JINJA_ENVIRONMENT.get_template('/templates/index.html')
            self.response.write(template.render(template_values))

    def post(self):
        try:
            url = self.request.POST["url"]
            try:
                c = HtmlToTextMain3()
                page = url
                texto = c.main(page)
            except ValueError:
                texto = "Incorrect Url!!!"
            except:
                print traceback.format_exc()
                texto = traceback.format_exc()            
            print "   "
            print url
            print "   "
            template_values = {
                'comentarios': texto,
            }
            template = JINJA_ENVIRONMENT.get_template('/templates/comentarios.html')
            self.response.write(template.render(template_values))

        except:
            print traceback.format_exc()
            error = traceback.format_exc()
            template_values = {
                'error': error,
            }
            template = JINJA_ENVIRONMENT.get_template('/templates/index.html')
            self.response.write(template.render(template_values))


class ComentariosArticulo(webapp2.RequestHandler):
    def get(self, url):
        try:
            url = url
            template_values = {
                'comentarios': url,
            }

            template = JINJA_ENVIRONMENT.get_template('/templates/comentarios-articulo.html')
            self.response.write(template.render(template_values))
        except:
            error = traceback.format_exc()
            template_values = {
                'error': error,
            }
            template = JINJA_ENVIRONMENT.get_template('/templates/index.html')
            self.response.write(template.render(template_values))

    def post(self):
        try:
            url = self.request.POST["url"]
            try:
                c = HtmlToTextMain()
                page = url
                texto = c.main(page)
            except:
                print traceback.format_exc()
                texto = traceback.format_exc()            
            print "   "
            print [url]
            print "   "

            self.response.headers['Content-Type'] = 'application/json'   
            obj = {
              'data': texto, 
            } 
            self.response.out.write(json.dumps(obj))

        except:
            print traceback.format_exc()
            error = traceback.format_exc()
            template_values = {
                'error': error,
            }
            template = JINJA_ENVIRONMENT.get_template('/templates/index.html')
            self.response.write(template.render(template_values))


class TestHtml(webapp2.RequestHandler):
    def get(self):
        try:
            #o = ElObservador()
            #o = o.get()

            hoy = date.today()

            template = JINJA_ENVIRONMENT.get_template('/templates/mono2.html')
            self.response.write(template.render(locals()))
        except:
            error = traceback.format_exc()
            template_values = {
                'error': error,
            }
            template = JINJA_ENVIRONMENT.get_template('/templates/mono2.html')
            self.response.write(template.render(locals()))


class Extract(webapp2.RequestHandler):
    def get(self):
        try:
            template_values = {
                'empty': "hello",
            }

            template = JINJA_ENVIRONMENT.get_template('/templates/comentarios.html')
            self.response.write(template.render(template_values))
        except:
            error = traceback.format_exc()
            template_values = {
                'error': error,
            }
            template = JINJA_ENVIRONMENT.get_template('/templates/index.html')
            self.response.write(template.render(template_values))

    def post(self):
        try:
            url = self.request.POST["url"]
            try:
                c = HtmlToTextMain5()
                page = url
                texto = c.main(page)
            except ValueError:
                texto = "Incorrect Url!!!"
            except:
                print traceback.format_exc()
                texto = traceback.format_exc()            
            print "   "
            print url
            print "   "
            template_values = {
                'comentarios': texto,
            }
            template = JINJA_ENVIRONMENT.get_template('/templates/comentarios.html')
            self.response.write(template.render(template_values))

        except:
            print traceback.format_exc()
            error = traceback.format_exc()
            template_values = {
                'error': error,
            }
            template = JINJA_ENVIRONMENT.get_template('/templates/index.html')
            self.response.write(template.render(template_values))


config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': '',
}


app = webapp2.WSGIApplication([
    webapp2.Route(r'/', Comentarios),
    webapp2.Route(r'/api/', ComentariosArticulo),
    webapp2.Route(r'/api/', ComentariosArticulo)
], config=config, debug=False)

app.error_handlers[404] = handle_404
app.error_handlers[500] = handle_500


def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()
