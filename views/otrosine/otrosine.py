# -*- coding: utf-8 -*-
import cgi
import os
import re
import json
import webapp2
import jinja2
import traceback
import urllib, urllib2
import httplib
import time


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__).replace("views/otrosine","")),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True,
)

class Otrosine(webapp2.RequestHandler):
	''' '''
	def get(self):
		try:
			print os.path.dirname(__file__).replace("views/otrosine","")
			template = JINJA_ENVIRONMENT.get_template('/templates/otrosine/nosotros.html')
			self.response.write(template.render(locals()))
		except: 
			print traceback.format_exc()
			print os.path.dirname(__file__).replace("/otrosine")
			return True