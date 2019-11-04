#+ -*- coding: utf-8 -*-
from google.appengine.ext import ndb
from models.models import News, NewsSelect
import webapp2
import traceback
import sys
import time
from datetime import date
import main


class Select(webapp2.RequestHandler):
	''' '''
	def list_black(self, key):
		try:
			exist = ListBlacke.query().get()
			if not exist:
				k = ListBlacke(
					keys = [key],
				)
				k.put()
				keys = k.keys
			else:
				keys = exist.keys

				if key not in keys:
					exist.keys.append(key)
					exist.put()
					keys = exist.keys

			return keys
		except:
			return traceback.format_exc()


	def truncate_words(self, keyword):
		for g in keyword:
				if " " in g: 
					sub_k = g.split()
					for t in range(0,len(sub_k)): 
						keyword.append(sub_k[t])
		return keyword


	def get(self):
		hoy = date.today()
		last = News.query(
			News.date == hoy,
		).order(News.id).get()
		# MONTVIDEO COM
		mc = News.query(
			News.date == hoy,
			News.news_from == "montevideo_com",
			News.in_use == False,
		).order(News.id)
		ep = News.query(
			News.date == hoy,
			News.news_from == "el_pais",
			News.in_use == False,
		).order(News.id)
		cont = self.selector_news(ep, mc, "el_pais", "montevideo_com")
		# EL OBSERVADOR
		print "\n"
		print "1 vuelta"
		print "cont"
		print cont
		eo2 = News.query(
			News.date == hoy,
			News.news_from == "el_observador",
			News.in_use == False,
		).order(News.id)
		mc2 = News.query(
			News.date == hoy,
			News.news_from == "montevideo_com",
			News.in_use == False,
		).order(News.id)
		cont2 = self.selector_news(eo2, mc2, "el_observador", "montevideo_com", cont)
		print "\n"
		print "2 vuelta"
		print "cont"
		print cont2
		# CIENTO OCHENTA
		co3 = News.query(
			News.date == hoy,
			News.news_from == "ciento_ochenta",
			News.in_use == False,
		).order(News.id)
		mc3 = News.query(
			News.date == hoy,
			News.news_from == "montevideo_com",
			News.in_use == False,
		).order(News.id)
		cont3 = self.selector_news(co3, mc3, "ciento_ochenta", "montevideo_com", cont2)
		print "\n"
		print "3 vuelta"
		print "cont"
		print cont3

		# UY PRESS
		co35 = News.query(
			News.date == hoy,
			News.news_from == "uy_press",
			News.in_use == False,
		).order(News.id)
		mc35 = News.query(
			News.date == hoy,
			News.news_from == "montevideo_com",
			News.in_use == False,
		).order(News.id)
		cont35 = self.selector_news(co35, mc35, "uy_press", "montevideo_com", cont3)
		print "\n"
		print "3.5 vuelta"
		print "cont"
		print cont35

		eo4 = News.query(News.date == hoy,News.news_from == "el_observador",News.in_use == False,
		).order(News.id)
		ep4 = News.query(
			News.date == hoy,
			News.news_from == "el_pais",
			News.in_use == False,
		).order(News.id)
		cont4 = self.selector_news(eo4, ep4, "el_observador", "el_pais", cont3)

		eo45 = News.query(
			News.date == hoy,
			News.news_from == "uy_press",
			News.in_use == False,
		).order(News.id)
		ep45 = News.query(
			News.date == hoy,
			News.news_from == "el_pais",
			News.in_use == False,
		).order(News.id)
		cont45 = self.selector_news(eo4, ep4, "uy_press", "el_pais", cont4)
		print "\n"
		print "45 vuelta"
		print "cont"
		print cont4
		co5 = News.query(
			News.date == hoy,
			News.news_from == "ciento_ochenta",
			News.in_use == False,
		).order(News.id)
		ep5 = News.query(
			News.date == hoy,
			News.news_from == "el_pais",
			News.in_use == False,
		).order(News.id)
		cont5 = self.selector_news(co5, ep5, "ciento_ochenta", "el_pais", cont45)
		print "\n"
		print "5 vuelta"
		print "cont"
		print cont5
		eo6 = News.query(
			News.date == hoy,
			News.news_from == "el_observador",
			News.in_use == False,
		).order(News.id)
		co6 = News.query(
			News.date == hoy,
			News.news_from == "ciento_ochenta",
			News.in_use == False,
		).order(News.id)
		cont6 = self.selector_news(co6, eo6, "ciento_ochenta", "el_observador", cont5)

		eo7 = News.query(
			News.date == hoy,
			News.news_from == "el_observador",
			News.in_use == False,
		).order(News.id)
		co7 = News.query(
			News.date == hoy,
			News.news_from == "uy_press",
			News.in_use == False,
		).order(News.id)
		cont7 = self.selector_news(co6, eo6, "uy_press", "el_observador", cont6)

		print "\n"
		print "7 vuelta"
		print "cont"
		print cont7

		eo8 = News.query(
			News.date == hoy,
			News.news_from == "ciento_ochenta",
			News.in_use == False,
		).order(News.id)
		co8 = News.query(
			News.date == hoy,
			News.news_from == "uy_press",
			News.in_use == False,
		).order(News.id)
		cont8 = self.selector_news(co6, eo6, "uy_press", "ciento_ochenta", cont7)

		print "\n"
		print "8 vuelta"
		print "cont"
		print cont8
		
		hoy = date.today()

		return True
		query = NewsSelect.query().order(NewsSelect.id)

		template_values = {
			"data": query,
			"fecha": hoy,
		}
		template = main.JINJA_ENVIRONMENT.get_template('/templates/profile.html')
		self.response.write(template.render(template_values))

	def selector_news(self, data, data2, news_from, news_from2, cont=0):
		try:
			hoy = date.today()
			last = News.query(
				News.date == hoy,
			).order(News.id).get()

			list_keyword_data = []
			for i in data:
				keyword = i.keyword
				title = i.title
				keys = (i.key).urlsafe()
				d = {
					"keyword": i.keyword,
					"title": i.title,
					"subtitle": i.subtitle,
					"url": i.url,
					"image": i.image,
					"category": i.category,
					"key": i.key,
				}
				list_keyword_data.append(d)
			print "entrando"
			if int(cont) > 0: cont = int(cont)
			else: cont = 0 
			for i in data2:
				keyword_data2 = i.keyword
				for e in list_keyword_data:
					key = e["keyword"]
					if key and keyword_data2:
						a = set(keyword_data2)
						b = set(key)
						if a.intersection(b):
							c = a.intersection(b)
							if len(c) > 2:
								print "similar"
								similar_data = {
									"title": e["title"],
									"subtitle": e["subtitle"],
									"image": e["image"],
									"url": e["url"],
									"category": e["category"],
									"news_from": news_from,
								}
								exist = NewsSelect.query(
									NewsSelect.title == i.title,
									NewsSelect.news_from == news_from2,
									NewsSelect.date == hoy,
									NewsSelect.is_similar == True,
								).get()

								if not exist:
									cont += 1
									save_me = NewsSelect(
										title = i.title,
										subtitle = i.subtitle,
										image = i.image,
										url = i.url,
										category = i.category,
										news_from = news_from2,
										html = i.html,
										similar = [similar_data],
										cant_similar = 1,
										keyword_set = [c],
										keyword = [keyword_data2, key],
										is_similar = True,
										id = cont,
										hour = last.hour,
									)
									save_me.put()
									print "post save"
									in_use = News.query(News.key == e["key"]).get()
									in_use.in_use = True
									in_use.put()

								else:
									cont += 1
									exist.similar.append(similar_data)
									exist.cant_similar = exist.cant_similar + 1
									exist.keyword_set.append(c)
									exist.keyword.append(key)
									exist.id = cont
									exist.hour = last.hour
									exist.put()

									in_use = News.query(News.key == e["key"]).get()
									in_use.in_use = True
									in_use.put()
								similar_data = {}
			return cont
		except:
			print traceback.format_exc()
			return traceback.format_exc()


	