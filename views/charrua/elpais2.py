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

from webapp2_extras import sessions
from bs4 import BeautifulSoup

from monkeylearn import Mk
from save import SaveNews


class Elpais2(webapp2.RequestHandler):
	''' '''
	def get(self):
		pass
	def main(self):
		try:
			page = "http://www.elpais.com.uy/"
			sock = urllib2.urlopen(page)
			htmlSource = sock.read()
			sock.close()
			soup = BeautifulSoup(htmlSource, "html.parser")
			portada = soup.find_all("div",attrs={"class": "article"})
			t = []
			c = 0
			for i in portada:
				print t.append()
		except: 
			print portada
			return traceback.format_exc()

            
            
            
            
            
 