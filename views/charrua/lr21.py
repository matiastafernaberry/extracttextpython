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


class Lr21(webapp2.RequestHandler):
	''' '''
	def get(self):
		try:
			page = "http://www.lr21.com.uy/"
			try:
				hdr = {'User-Agent':'Mozilla/5.0'}
				req = urllib2.Request(page,headers=hdr)

				sock = urllib2.urlopen(req)
			except:
				print traceback.format_exc()
			htmlSource = sock.read()
			sock.close()
			soup = BeautifulSoup(htmlSource, "html.parser")
			portada = soup.find_all("article",attrs={"class": "article"})

			#print portada
			t = []
			c = 0
			for i in portada:
				try:
					print ""
					a = i
					#print a

					### link ###
					try:
						url = i.find_all("a")
						url = url[0]["href"]
						print ""
						print url
						print ""
					except:
						print traceback.format_exc()
						url = ""

					### image ###
					try:
						image = i.find_all("img")
						image = image[0]
						image = str(image).replace("data-src","src")
						image = str(image)
						image = image[:5] + "class='img-responsive'" + image[4:]
						#image = BeautifulSoup(image, "html.parser")
						print ""
						print image
						print ""
					except:
						print traceback.format_exc()
						image = ""

					### title ###
					try:
						article = i.find_all("div",attrs={"class": "article-title"})
						category = article[0].find_all("div",attrs={"class": "xx"})[0].string
						print [category] 
						print ""
						title = article[0].h2.string
						print [title]
						print ""
					except:
						print traceback.format_exc()
						title = ""

					### subtitulo ###
					try:
						subtitle = article[0].li.string
						print [subtitle]
						print ""
					except:
						print traceback.format_exc()
						subtitle = ""

					e = SaveNews()
					e = e.if_exist(title, "lr21", c)
					if e:
						print "EXISTE"
						c = c + 1
						#print i
						continue

					# TEXT EXTRACT
					# TEXT EXTRACT
					try:
						print "pre mk"
						text = HtmlToTextMain()
						text = text.main(url)
						print text
						
						print "post mk"
					except: 
						print text
						print traceback.format_exc()
						continue

					try:
						print "PRE SAVE"
						s = SaveNews()
						sav = s.saveme(
							title = title,
							subtitle = "",
							image = image,
							url = url,
							category = category,
							keyword = [],
							news_from = "lr21",
							id = c,
							html = text,
						)
						print "SAVE"

					except:
						print traceback.format_exc()
						continue

					print "sleep"
					time.sleep(2)
					print "wake up"

					c += 1
					print c

					#break

				except:
					print i
					print traceback.format_exc()
					continue
					
				#break
			return t
		except: 
			print traceback.format_exc()
			return traceback.format_exc()
			

            
            
            
            
            
 