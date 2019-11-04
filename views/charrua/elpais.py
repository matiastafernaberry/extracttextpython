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

from views.htmltotext.htmltotext3 import HtmlToTextMain
from save import SaveNews


class Elpais(webapp2.RequestHandler):
	''' '''
	def get(self):
		try:
			print "el pais"
			page = "http://www.elpais.com.uy/"
			try:
				hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       				'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       				'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       				'Accept-Encoding': 'none',
       				'Accept-Language': 'en-US,en;q=0.8',
       				'Connection': 'keep-alive'}
				req = urllib2.Request(page,headers=hdr)
				sock = urllib2.urlopen(req)
			except:
				print traceback.format_exc()

			htmlSource = sock.read()
			sock.close()
			soup = BeautifulSoup(htmlSource, "html.parser")
			portada = soup.find_all("article")
		
			t = []
			c = 0
			for i in portada:
				try:
					print "entro "
					#if c == 3: break
					try:
						url = i.find_all("a")[0]["href"]
						url = "http://www.elpais.com.uy" + url
						print url
					except:
						print traceback.format_exc()
					
					### tag ###
					try:
						tag = i.find_all("div",attrs={"class": "supratitle"})[0].a.string
						print [tag]
					except:
						tag = ""
						print traceback.format_exc()
					### url ###
					try:
						title = i.find_all("h1",attrs={"class": "title"})[0].a.string
						print [title]
					except:
						try:
							title = i.find_all("h2",attrs={"class": "title"})[0].a.string
							print [title]
						except:
							try:
								title = i.find_all("h2",attrs={"class": "title"})[0].a.string
								print [title]
							except:
								title = ""
								print traceback.format_exc()

					print "  URL  "
					### image ###
					try:
						image = i.find_all("div",attrs={"class": "image-container"})[0].img["data-src"]
						image = "<img class='lazy' src='" + image + "' alt='" + title + "'>"
						print image
					except:
						print traceback.format_exc()

					

					e = SaveNews()
					e = e.if_exist(title, "el_pais", c, url)
					#e = False
					if e:
						print "EXISTE"
						c = c + 1
						#print i
						continue

					# TEXT EXTRACT
					try:
						print "pre mk"
						text = HtmlToTextMain()
						text = text.main(url)
						#print [text]
						#if c == 10: break
						print "post mk"
					except: 
						print [text]
						print traceback.format_exc()
						continue
					# keyword extract

					try:
						print "PRE SAVE"
						s = SaveNews()
						sav = s.saveme(
							title = title,
							subtitle = "",
							image = image,
							url = url,
							category = tag,
							keyword = [],
							news_from = "el_pais",
							id = c,
							html = text,
						)
						c = c + 1
						print c
						print "SAVE"
					except:
						print traceback.format_exc()
						continue
					print "sleep"
					time.sleep(2)
					print "wake up"
				except:
					print i
					print traceback.format_exc()
					continue
				#break
			return True
		except: 
			print traceback.format_exc()
			return True

            
            
            
            
            
 