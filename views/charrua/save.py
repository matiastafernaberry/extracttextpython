# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
from models.models import News3
import webapp2
import traceback
import sys
import time
from datetime import date


class SaveNews(webapp2.RequestHandler):
	''' '''
	def if_exist(self, title, news_from, id=None, url=""):
		try:
			if isinstance(title, unicode): pass
			else: title = title.decode('utf-8')
		except: print traceback.format_exc() 
		hoy = date.today()
		#edit = (ndb.Key("News", date==hoy)).urlsafe()# obtiene la key
		#print edit
		#e = News.query(ndb.GenericProperty("__key__ =") == edit)# filtra por la key
		#print e
		#sys.exit()
		edit = News3.query(
			News3.url == url,
			News3.news_from == news_from,
			News3.date == hoy,
		).get()
		#edit = edit.get()
		#print edit.date
		#print [edit.title]
		#print edit.news_from
		#print edit
		#f = News.query(News.news_from == news_from,News.date == hoy,).get()
		#edit = f.filter(ndb.GenericProperty('news_from') == news_from)
		#print f
		#sys.exit()
		if edit: 
			edit.id = int(id)
			edit.put()
			print "Exist and update"
			return True
		else: 
		    print "No exist"
		    return False

	def similitude(self, news_from):
		try:
			hoy = date.today()
			edit = News3.query(
				#News.title == title,
				News3.news_from != news_from,
				News3.date == hoy,
			).fetch()

			for i in edit:
				print i.keyword

			sys.exit()
		except:
			print traceback.format_exc() 
			return traceback.format_exc() 

	def saveme(self, news_from, title, subtitle, image, url, category, keyword, id, html):
		try:
			try:
				if isinstance(title, unicode): pass
				else: title = title.decode('utf-8')
			except: pass
			if not category: category = ""

			print "pre save"
			hora = int(time.strftime("%H"))
			d = {
				"news_from":news_from,
				"title":title,
				"subtitle":subtitle,
				"image":image,
				"url":url,
				"category":category,
				"keyword":keyword,
				"hora":hora,
				"html":[html]
			}
			print " "
			try:
				if isinstance(image, unicode): pass
				else: image = image.decode('utf-8')
			except:
				image = str(image)
				print type(image)

			if news_from == "uy_press":
				if ",57" in str(url): category = "deportes"
				if ",6" in str(url): category = "politica"

			sav = News3(
				news_from = news_from,
				title = title,
				subtitle = subtitle,
				image = image,
				url = url,
				category = category,
				keyword = keyword,
				id = int(id),
				html = unicode(html),
				hour = hora,
			)
			sav.put()
			print "!!!SAVE!!!"
			return True
		except:
			print traceback.format_exc()
			return False