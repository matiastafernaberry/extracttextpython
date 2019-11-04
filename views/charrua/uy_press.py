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
import main
from datetime import date,datetime, timedelta
from google.appengine.ext import ndb
from models.models import News3

from webapp2_extras import sessions
from bs4 import BeautifulSoup

from views.htmltotext.htmltotext import HtmlToTextMain
from models.models import *
from save import SaveNews


if os.name == 'nt':
	stringReplace = "views\charrua"
else:
	stringReplace = "views/charrua"

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__).replace(stringReplace,"")),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True,
)


class UypressM(webapp2.RequestHandler):
    def get(self, idd):
        try:
            #c = UyPress()
            #idd = self.request.get('idd')
            print idd
            #c = c.get()
            print "uy press"
            hoy = date.today()
            try:
                data = News3.query(
                    #News3.date == hoy,
                    News3.key == ndb.Key(News3, int(idd)),
                )
            except:
                print traceback.format_exc()

            dia = hoy.strftime('%d')
            mes= hoy.strftime('%m')
            year= hoy.strftime('%Y')
            week_day = datetime.today().weekday()
            days_week = ["Lunes","Martes","MiÃ©rcoles","Jueves","Viernes","SÃ¡bado","Domingo"]
            week_day = days_week[week_day]
            hora = hoy - timedelta(hours=3)
            hora = hora.strftime("%H:%M:%S")

            try:
                clima = Yahoo()
                cli = clima.get()
            except: cli = ""

            template_values = {
                'data': data,
                'clima': cli,
                'dia': dia,
                'mes': mes,
                'year': year,
                'week_day': week_day,
                'hora':hora,
            }

            template = JINJA_ENVIRONMENT.get_template('/templates/mono4.html')
            self.response.write(template.render(template_values))
        except:
            error = traceback.format_exc()
            print error
            template_values = {
                'error': error,
            }
            template = JINJA_ENVIRONMENT.get_template('/templates/mono5.html')
            self.response.write(template.render(template_values))


class UyPress(webapp2.RequestHandler):
	def get(self):
		try:
			page = "http://www.uypress.net/index_1.html"
			sock = urllib2.urlopen(page)
			htmlSource = sock.read()
			sock.close()
			soup = BeautifulSoup(htmlSource, "html.parser")
			# solo la portada
			portada = soup.find_all("div", attrs={"class": "ucppal divslide"})
			l = []
			c = 0
			for i in portada:
				try:
					a = i.find_all("a")[0]
					title = (i.find_all("a")[1]).string
					subtitle = (i.find_all("h2")[0]).string
					category = (i.find_all("h3")[0]).string
					if (category == "Política"): category = "politica"
					url = a["href"]
					img = a.find_all("img")[0]
					src = img["src"]
					img = "<img class='img-responsive' src='" + src + "' />"
					
					e = SaveNews()
					e = e.if_exist(title, "uy_press", c, url)

					if e:
						print "EXISTE"
						c = c + 1
						#print i
						continue

					try:
						print "pre mk"
						text = HtmlToTextMain()
						text = text.main(url)
						
						#print text
						
						
						print ""
						print text
						print "post mk"
					except: 
						#print text
						print traceback.format_exc()
						continue

					#break
					try:
						print "PRE SAVE"
						s = SaveNews()
						sav = s.saveme(
							title = title,
							subtitle = subtitle,
							image = img,
							url = url,
							category = category,
							keyword = [],
							news_from = "uy_press",
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

				except: return traceback.format_exc()
			
			# subportada de la pagina
			subportada = soup.find_all("div", attrs={"class": "trescolhome_noticias"})
			c = 0
			for i in subportada:
				#break
				try:
					a = i.find_all("a")[0]
					title = (i.find_all("a")[1]).string
					url = a["href"]
					img = a.find_all("img")[0]
					src = img["src"]
					img = "<img src='" + src + "' />"
					category = (i.find_all("h2")[0]).string
					#print [category]
					subtitle = (i.find_all("h2")[1]).string
					#print [subtitle]
					# d = {
					# 	"title": title,
					# 	"subtitle": subtitle,
					# 	"url": url,
					# 	"image": img,
					# 	"category": category,
					# }
					# l.append(d)
					e = SaveNews()
					e = e.if_exist(title, "uy_press", c, url)
					if e:
						print "EXISTE"
						#print i
						continue
					try:
						print "pre mk"
						text = HtmlToTextMain()
						text = text.main(url)
						print "post mk"
					except: 
						#print text
						print traceback.format_exc()
						continue
					
					try:
						print "PRE SAVE"
						s = SaveNews()
						sav = s.saveme(
							title = title,
							subtitle = subtitle,
							image = img,
							url = url,
							category = category,
							keyword = [],
							news_from = "uy_press",
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
				except: 
					print traceback.format_exc()
					return traceback.format_exc()
			# resto
			resto = soup.find_all("div", attrs={"class": "seccioneshome_noticias"})
			c = 0
			for i in resto:
				#break
				try:
					a = i.find_all("a")[0]
					# title
					try:
						title = (i.find_all("a")[1]).string
					except:
						title = (i.find_all("a")[0])
						title = title.string

					url = a["href"]
					# category
					try:
						category = (i.find_all("h1")[0]).string
					except: category = ""
					# image
					try:
						img = a.find_all("img")[0]
					except:
						img = a.find_all("img")
						if not img: img = None
						else:
							src = img["src"]
							img = "<img src='" + src + "' />"
					if img:
						src = img["src"]
						img = "<img src='" + src + "' />"
						
					subtitle = (i.find_all("h2")[0]).string
					#print [subtitle]
					#break
					# d = {
					# 	"title": title,
					# 	"subtitle": subtitle,
					# 	"url": url,
					# 	"image": img,
					# 	#"category": category,
					# }
					# l.append(d)
					e = SaveNews()
					e = e.if_exist(title, "uy_press", c, url)
					if e:
						print "EXISTE"
						#print i
						continue
					try:
						print "pre mk"
						text = HtmlToTextMain()
						text = text.main(url)
						print "post mk"
					except: 
						#print text
						print traceback.format_exc()
						continue
					
					try:
						print "PRE SAVE"
						s = SaveNews()
						sav = s.saveme(
							title = title,
							subtitle = subtitle,
							image = img,
							url = url,
							category = "",
							keyword = [],
							news_from = "uy_press",
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
				except: 
					return traceback.format_exc()

			return True

		except: 
			return traceback.format_exc()


class UypressPolitica(webapp2.RequestHandler):
	def get(self):
		try:
			page = "http://www.uypress.net/acategoria.aspx?6"
			sock = urllib2.urlopen(page)
			htmlSource = sock.read()
			sock.close()
			soup = BeautifulSoup(htmlSource, "html.parser")
			# solo la portada
			portada = soup.find_all("div", attrs={"id": "principalUC"})
			portada = portada[0].find_all("div")
			l = []
			c = 0
			for i in portada:
				try:
					print " "
					print c
					if (c == 0): 
						c += 1
						continue

					url = i.find_all("a")[0]["href"]
					title = (i.find_all("a")[0]).string
					print [title]
					category = "politica"
					img = ""
					try:
						#e = SaveNews()
						#e = e.if_exist(title, "uy_press_politica", c, url)
						edit = News3.query(
							News3.url == url,
							News3.news_from == "uy_press_politica",
						).get()
						if edit: 
							print "Existe"
							c = c + 1
							#print i
							continue
						else: print "No Existe"

					except:
						print traceback.format_exc()


					try:
						print "pre mk"
						text = HtmlToTextMain()
						text = text.main(url)
						#print text
						print ""
						print [text]
						print "post mk"
					except: 
						#print text
						print traceback.format_exc()
						continue

					#break
					try:
						print "PRE SAVE"
						s = SaveNews()
						sav = s.saveme(
							title = title,
							subtitle = "",
							image = "",
							url = url,
							category = category,
							keyword = [],
							news_from = "uy_press_politica",
							id = c,
							html = text,
						)
						print "SAVE"
						print sav
					except:
						print traceback.format_exc()
						continue

					print "sleep"
					time.sleep(2)
					print "wake up"

					c += 1
					print c

				except: 
					print traceback.format_exc()
					return traceback.format_exc()
		except:
			print traceback.format_exc() 
			return traceback.format_exc()


class UypressEconomia(webapp2.RequestHandler):
	def get(self):
		try:
			page = "http://www.uypress.net/acategoria.aspx?77"
			sock = urllib2.urlopen(page)
			htmlSource = sock.read()
			sock.close()
			soup = BeautifulSoup(htmlSource, "html.parser")
			# solo la portada
			portada = soup.find_all("div", attrs={"id": "principalUC"})
			portada = portada[0].find_all("div")
			l = []
			c = 0
			for i in portada:
				try:
					print " "
					print c
					if (c == 0): 
						c += 1
						continue

					url = i.find_all("a")[0]["href"]
					title = (i.find_all("a")[0]).string
					print [title]
					category = "economia"
					img = ""
					try:
						#e = SaveNews()
						#e = e.if_exist(title, "uy_press_politica", c, url)
						edit = News3.query(
							News3.url == url,
							News3.news_from == "uy_press_economia",
						).get()
						if edit: 
							print "Existe"
							c = c + 1
							#print i
							continue
						else: print "No Existe"

					except:
						print traceback.format_exc()


					try:
						print "pre mk"
						text = HtmlToTextMain()
						text = text.main(url)
						#print text
						print ""
						print [text]
						print "post mk"
					except: 
						#print text
						print traceback.format_exc()
						continue

					#break
					try:
						print "PRE SAVE"
						s = SaveNews()
						sav = s.saveme(
							title = title,
							subtitle = "",
							image = "",
							url = url,
							category = category,
							keyword = [],
							news_from = "uy_press_economia",
							id = c,
							html = text,
						)
						print "SAVE"
						print sav
					except:
						print traceback.format_exc()
						continue

					print "sleep"
					time.sleep(2)
					print "wake up"

					c += 1
					print c

				except: 
					print traceback.format_exc()
					return traceback.format_exc()
		except:
			print traceback.format_exc() 
			return traceback.format_exc()


class UypressDeportes(webapp2.RequestHandler):
	def get(self):
		try:
			page = "http://www.uypress.net/acategoria.aspx?57"
			sock = urllib2.urlopen(page)
			htmlSource = sock.read()
			sock.close()
			soup = BeautifulSoup(htmlSource, "html.parser")
			# solo la portada
			portada = soup.find_all("div", attrs={"id": "principalUC"})
			portada = portada[0].find_all("div")
			l = []
			c = 0
			for i in portada:
				try:
					print " "
					print c
					if (c == 0): 
						c += 1
						continue

					url = i.find_all("a")[0]["href"]
					title = (i.find_all("a")[0]).string
					print [title]
					category = "deportes"
					img = ""
					try:
						#e = SaveNews()
						#e = e.if_exist(title, "uy_press_politica", c, url)
						edit = News3.query(
							News3.url == url,
							News3.news_from == "uy_press_deportes",
						).get()
						if edit: 
							print "Existe"
							c = c + 1
							#print i
							continue
						else: print "No Existe"

					except:
						print traceback.format_exc()


					try:
						print "pre mk"
						text = HtmlToTextMain()
						text = text.main(url)
						#print text
						print ""
						print [text]
						print "post mk"
					except: 
						#print text
						print traceback.format_exc()
						continue

					#break
					try:
						print "PRE SAVE"
						s = SaveNews()
						sav = s.saveme(
							title = title,
							subtitle = "",
							image = "",
							url = url,
							category = category,
							keyword = [],
							news_from = "uy_press_deportes",
							id = c,
							html = text,
						)
						print "SAVE"
						print sav
					except:
						print traceback.format_exc()
						continue

					print "sleep"
					time.sleep(2)
					print "wake up"

					c += 1
					print c

				except: 
					print traceback.format_exc()
					return traceback.format_exc()
		except:
			print traceback.format_exc() 
			return traceback.format_exc()

			