import sys
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

from bs4 import BeautifulSoup



class Mk(webapp2.RequestHandler):
	"""docstring for ClassName"""

	def monkey_learn_text_extract(self, url):
		try:
			#print url
			hdr = {'User-Agent':'Mozilla/5.0'}
			req = urllib2.Request(url,headers=hdr)
			sock = urllib2.urlopen(req)
			htmlSource = sock.read()
			sock.close()
			data = BeautifulSoup(htmlSource, "html.parser")
			data = {'text_list': [unicode(data)]}
			site = "https://api.monkeylearn.com/v2/extractors/ex_RK5ApHnN/extract/"
			headers = {
				'Authorization':'Token 29cde5a7018231744078d3714ed64d8b51ac543e',
				'Content-Type': 'application/json'
			}
			req = urllib2.Request(site, json.dumps(data), headers)
			sock = urllib2.urlopen(req)
			data = sock.read()
			sock.close()
			data = json.loads(data)
			data = data["result"][0]
			t = []
			for i in data: t.append(i["paragraph_text"])
			text = " ".join(t)
			if isinstance(text, unicode): pass
			else: text = text.decode('utf-8')
			return text
		except:
			print traceback.format_exc()
			return False


	def monkey_learn_entities_extract(self, data):
		try:
			#print url
			data = {'text_list': [unicode(data)]}
			site = "https://api.monkeylearn.com/v2/classifiers/cl_6hvxGfLu/classify/"
			headers = {
				'Authorization':'Token 29cde5a7018231744078d3714ed64d8b51ac543e',
				'Content-Type': 'application/json'
			}
			req = urllib2.Request(site, json.dumps(data), headers)
			sock = urllib2.urlopen(req)
			data = sock.read()
			sock.close()
			data = json.loads(data)

			data = data["result"]
			return data
			t = []
			for i in data: t.append(i["entity"])
			
			return t
		except:
			print traceback.format_exc()
			return False


	def monkey_learn_keyword_extract(self, data):
		try:
			if data:
				data = {'text_list': [unicode(data)]}
				# Keyword Extractor (Spanish)
				site = "https://api.monkeylearn.com/v2/extractors/ex_eV2dppYE/extract/"
				headers = {
					'Authorization':'Token 29cde5a7018231744078d3714ed64d8b51ac543e',
					'Content-Type': 'application/json'
				}
				
				req = urllib2.Request(site, json.dumps(data), headers)
				sock = urllib2.urlopen(req)
				data = sock.read()
				sock.close()
				data = json.loads(data)
				data = data["result"][0]
				ke = []
				for e in data: ke.append((e["keyword"]).lower())
				return ke
			else: return False
		except:
			print data
			print traceback.format_exc()
			return False

	def my_text_extract(self, url):
		try:
			sock = urllib2.urlopen(url)
			htmlSource = sock.read()
			sock.close()   
			soup = BeautifulSoup(htmlSource, "html.parser")
			print soup
			return soup
		except:
			print traceback.format_exc()
			return False
	
