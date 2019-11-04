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
from datetime import date,datetime, timedelta

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import ndb
from models.models import News3
from views.htmltotext.htmltotext import HtmlToTextMain
import webapp2
import main
from webapp2_extras import sessions
from bs4 import BeautifulSoup

from models.models import News
from save import SaveNews
from monkeylearn import Mk

if os.name == 'nt':
    stringReplace = "views\charrua"
else:
    stringReplace = "views/charrua"

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__).replace(stringReplace,"")),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True,
)


class SubrayadoMain(webapp2.RequestHandler):
    def get(self):
        try:
            # manejar error HTTP
            error = []
            page = "http://subrayado.com.uy/"
            sock = urllib2.urlopen(page)
            htmlSource = sock.read()
            sock.close()   
            soup = BeautifulSoup(htmlSource, "html.parser")
            data = soup.find_all("article")
            l = []; c = 0
            for u in data: 
                try:
                    # TITLE
                    print ""
                    print c
                    print u
                    # url
                    try:
                        url = u.find_all("a")[0]["href"]
                    except:
                        print traceback.format_exc()
                        continue
                    # category
                    try:
                        category = u.find_all("span")[0].string
                    except: 
                        print traceback.format_exc()
                        continue
                    # image                       
                    try: 
                        image = u.find_all("img")[0]
                        src = image["src"]
                        image = "<img class='img-responsive' src='" + src + "' />"
                    except: 
                        print traceback.format_exc()
                        continue
                    # title
                    try:
                        title = u.find_all(
                            "div",attrs={"class": "info-wrapper"}
                        )[0].find_all("a")[0].string
                    except: 
                        print traceback.format_exc()
                        continue                    
                    
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
                    
                    # TEXT EXTRACT
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
                    
                    savemi = SaveNews()
                    print "pre save"
                    save = savemi.saveme(
                        title = title, 
                        subtitle = "", 
                        image = image,
                        url = url,
                        category = category,
                        keyword = [],
                        news_from = "subrayado",
                        id = c,
                        html = text,
                    )
                    print save
                    c += 1
                    #l.append(d)
                    print c
                    print "sleep"
                    time.sleep(2)
                    print "wake up mf!" 
                except: 
                    print traceback.format_exc()
                    return traceback.format_exc()
            #return error
            return True
        #except httplib.HTTPException: 
        #    princ = Charrua()
        #    elobservador = princ.elobservador()
        except: 
            print traceback.format_exc()
            return False


class Subrayado(webapp2.RequestHandler):
    def get(self):
        try:
            #c = UyPress()
            print os.path.dirname(__file__).replace("charrua","")
            #c = c.get()
            print "uy press"
            hoy = date.today()
            try:
                data = News3.query(
                    News3.date == hoy,
                    News3.news_from == "subrayado",
                    #News3.category == "politica"
                ).order(News3.id).order(-News3.created)
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

            template = JINJA_ENVIRONMENT.get_template('/templates/mono2.html')
            self.response.write(template.render(template_values))
        except:
            error = traceback.format_exc()
            print error
            template_values = {
                'error': error,
            }
            template = JINJA_ENVIRONMENT.get_template('/templates/mono2.html')
            self.response.write(template.render(template_values))