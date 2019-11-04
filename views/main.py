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

from views.category import *

import webapp2
from webapp2_extras import sessions

reload(sys)  
sys.setdefaultencoding('utf8')

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__).replace("views","")),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True,
)

class KeyExtractTest(webapp2.RequestHandler):
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





