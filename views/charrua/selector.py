# -*- coding: utf-8 -*-
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
	def truncate_words(self, keyword):
		for g in keyword:
				if " " in g: 
					sub_k = g.split()
					for t in range(0,len(sub_k)): 
						keyword.append(sub_k[t])
		return keyword

	def query_news(self, diario):
		try:
			hoy = date.today()
			e = News.query(
				News.date == hoy,
				News.news_from == diario,
				News.in_use == False,
			).order(News.id)
			return e
		except:
			print traceback.format_exc()
			return traceback.format_exc()

	def post_selector(self):
		try:
			hoy = date.today()
			e = NewsSelect.query(
				NewsSelect.date == hoy,
				NewsSelect.is_similar == True,
			)
			for i in e:
				title = i.title
				for o in e:
					if title != o.title:
						keyword_set_a = i.keyword
						keyword_set_b = o.keyword

						a = set(keyword_set_a[0])
						a2 = set(keyword_set_a[1])
						b = set(keyword_set_b[0])
						b2 = set(keyword_set_b[1])
						if (a.intersection(b) or
							a.intersection(b2) or
							a2.intersection(b) or
							a2.intersection(b2)):

							c = a.intersection(b)
							c2 = a.intersection(b2)
							c3 = a2.intersection(b)
							c4 = a2.intersection(b2)
							if (len(c) > 2 or
								len(c2) > 2 or
								len(c3) > 2 or
								len(c4) > 2):
								try:
									in_use = NewsSelect.query(
										NewsSelect.title == i.title,
									).get()
									similar = {
										"keyword": in_use.keyword,
										"title": in_use.title,
										"subtitle": in_use.subtitle,
										"url": in_use.url,
										"image": in_use.image,
										"category": in_use.category,
									}
								except:
									print "\n"
									print [i.title]
									print traceback.format_exc()
									continue
								try:
									in_useb = NewsSelect.query(
										NewsSelect.title == o.title,
									).get()
									similarb = {
										"keyword": in_useb.keyword,
										"title": in_useb.title,
										"subtitle": in_useb.subtitle,
										"url": in_useb.url,
										"image": in_useb.image,
										"category": in_useb.category,
									}
								except:
									print "\n"
									print [o.title]
									print traceback.format_exc()
									continue

								if i.cant_similar >= o.cant_similar:
									in_use.similar.append(in_useb.similar[0])
									in_use.similar.append(similarb)
									in_use.cant_similar = in_use.cant_similar + 1
									in_use.keyword_set.append(keyword_set_b)
									#in_use.keyword.append(i.keyword)
									in_use.put()

									in_useb.key.delete()

									print "\n"
									print in_use
									print "\n"
									use = News.query(News.title == i.title).get()
									use.in_use = True
									use.put()
								else:
									in_useb.similar.append(in_use.similar[0])
									in_use.similar.append(similar)
									in_useb.cant_similar = in_useb.cant_similar + 1
									in_useb.keyword_set.append(keyword_set_a)
									#in_useb.keyword.append(o.keyword)
									in_useb.put()

									in_use.key.delete()

									print "\n"
									print in_useb
									print "\n"
									use = News.query(News.title == o.title).get()
									use.in_use = True
									use.put()					
			return webapp2.redirect('/')
		except:
			print traceback.format_exc()
			return traceback.format_exc()

	def get(self):
		hoy = date.today()
		last = News.query(
			News.date == hoy,
		).order(News.id).get()
		diarios = ["montevideo_com","el_observador","el_pais","ciento_ochenta","uy_press"]
		cont = 0
		for i in diarios:
			query = self.query_news(i)
			for e in diarios:
				if i != e:
					query2 = self.query_news(e)
					cont = self.selector_news(query,query2, i, e, cont)
			del diarios[0]

		post = self.post_selector()

		return webapp2.redirect('/')

		# query = NewsSelect.query().order(NewsSelect.id)

		# template_values = {
		# 	"data": query,
		# 	"fecha": hoy,
		# }
		# template = main.JINJA_ENVIRONMENT.get_template('/templates/profile.html')
		# self.response.write(template.render(template_values))

	def selector_news(self, data, data2, news_from, news_from2, cont=0):
		try:
			hoy = date.today()
			last = News.query(
				News.date == hoy,
			).order(News.id).get()

			list_keyword_data = []
			for i in data:
				d = {
					"keyword": i.keyword,
					"title": i.title,
					"subtitle": i.subtitle,
					"url": i.url,
					"image": i.image,
					"category": i.category,
					"key": i.key,
					"html": i.html,
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
									"html": e["html"],
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
									in_use = News.query(News.title == e["title"]).get()
									in_use.in_use = True
									in_use.put()
									print in_use.in_use
									
									
								else:
									cont += 1
									exist.similar.append(similar_data)
									exist.cant_similar = exist.cant_similar + 1
									exist.keyword_set.append(c)
									exist.keyword.append(key)
									exist.id = cont
									exist.hour = last.hour
									exist.put()

									in_use = News.query(News.title == e["title"]).get()
									in_use.in_use = True
									in_use.put()
									print in_use.in_use
								

								similar_data = {}
			return cont
		except:
			print traceback.format_exc()
			return traceback.format_exc()


	