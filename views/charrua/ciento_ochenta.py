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
import sys

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import ndb
import webapp2
import main
from webapp2_extras import sessions
from bs4 import BeautifulSoup

from models.models import News
from monkeylearn import Mk
from save import SaveNews


class CientoOchenta(webapp2.RequestHandler):
      def get(self):
            try:
                  page = "http://cientoochenta.com.uy/"
                  print "\n"
                  print "180"
                  print "\n"
                  #time.sleep(2)
                  #page = "http://www.contragolpe.com.uy/articulo/57192_la-zancadilla-de-un-camarografo-a-usain-bolt"
                  #page = "http://www.180.com.uy/articulo/57260_consejo-de-ministros-respaldo-levantar-esencialidad"
                  sock = urllib2.urlopen(page)
                  htmlSource = sock.read()
                  sock.close()   
                  soup = BeautifulSoup(htmlSource, "html.parser")
                  url = soup.find_all("div", attrs={"class": "notita"})
                  c = 0; l = []
                  for i in url:
                        #return i
                        try:
                              category = i.find_all("div", class_="header")
                              category = category[0].find_all("a")
                              category = category[0].string
                              if str(category) == "Fútbol":
                                    category = "deportes"
                              print category
                        except:
                              print traceback.format_exc()
                              return True
                        try:
                              image = i.find_all("img")
                              if image: 
                                    image = image[0]
                                    src = image["src"]
                                    image = "<img class='img-responsive' src='" + src + "' />"
                                    
                        except:
                              print traceback.format_exc()
                        try:
                              title_0 = i.find_all("div", class_="text")
                              title = title_0[0].find_all("a", class_="linkArticulo")
                              url = title[0]["href"]
                              if title: 
                                    title = title[0]
                                    title = title.string
                              #print [title]
                              #sys.exit()
                        except:
                              print traceback.format_exc()
                              continue


                        # exist
                        e = SaveNews()
                        e = e.if_exist(title, "ciento_ochenta", c, url)
                        if e:
                              print "EXIST"
                              c = c + 1
                              continue
                        else: print "NO EXISTE"

                        try:
                              subtitle = (i.find_all("h4"))[0].string
                              #print [subtitle]
                              #sys.exit()
                        except:
                              print traceback.format_exc()
                        
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
                        
                        print "pre save"
                        try:
                              s = SaveNews()
                              sav = s.saveme(
                                    title = title,
                                    subtitle = subtitle,
                                    image = image,
                                    url = url,
                                    category = category,
                                    keyword = keyword,
                                    news_from = "ciento_ochenta",
                                    id = c,
                                    html = text,
                              )

                              print "save"
                        except:
                              print traceback.format_exc()
                              continue
                        
                        #l.append(d)
                        print c
                        c = c + 1
                      
                  
                  return l
            except: 
                  print traceback.format_exc()
                  return traceback.format_exc()