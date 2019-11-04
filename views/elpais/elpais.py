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
from datetime import date,datetime, timedelta

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import ndb
from google.appengine.ext import gql

from webapp2_extras import sessions

from views.classification.testclassifier import TestClassifier

from views.htmltotext.htmltotext4 import HtmlToTextMain

import sys
reload(sys)  
sys.setdefaultencoding('utf8')



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname("/")),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True,
)


class ElpaisTalCualEs(webapp2.RequestHandler):
    def get(self):
        try:
            #print "hello"
            c = HtmlToTextMain()
            page = "http://www.elpais.com.uy/"
            o = c.main(page)

            template_values = {
                'data': o,
                
            }
            template = JINJA_ENVIRONMENT.get_template('/templates/profile2.html')
            self.response.write(template.render(template_values))
        except:
            print "  os  "
            oso = os.path.dirname(__file__)
            oso2 = str(oso).replace("views\\elpais"," ")

            print oso2
            #print str(oso2).replace("\\"," ", -1)
            error = traceback.format_exc()
            template_values = {
                'error': error,
            }
            template = JINJA_ENVIRONMENT.get_template('/templates/mono2.html')
            self.response.write(template.render(template_values))

    def post(self):
        try:
            print "hello to heaven my dumb mind"
            post_values = self.request.POST["url"]
            print post_values

            c = HtmlToTextMain()
            page = "http://www.elpais.com.uy/" + post_values
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




