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


class LaRepublica(webapp2.RequestHandler):
      def get(self):
            try:
                  page = "http://www.republica.com.uy/"
                  print "\n"
                  print "LaRepublica"
                  print "\n"
                  #time.sleep(2)
                  #page = "http://www.contragolpe.com.uy/articulo/57192_la-zancadilla-de-un-camarografo-a-usain-bolt"
                  #page = "http://www.180.com.uy/articulo/57260_consejo-de-ministros-respaldo-levantar-esencialidad"
                  sock = urllib2.urlopen(page)
                  htmlSource = sock.read()
                  sock.close()   
                  soup = BeautifulSoup(htmlSource, "html.parser")
                  url = soup.find_all("article", attrs={"id": re.compile("^post")})
                  c = 0; l = []
                  for i in url:
                        category = (i.find_all("p",attrs={"class": "colgado"}))[0].string
                        image = (i.find_all("img", attrs={"class": re.compile("^attachment-post-thumbnail")}))[0]
                        src =  image["src"]
                        image = "<img src='" + src + "'/>"
                        title = (i.find_all("a",attrs={"rel": "bookmark"}))[0]
                        url = str(title["href"])
                        title = title.string
                        
                        e = SaveNews()
                        e = e.if_exist(title, "la_republica")
                        if e:
                              print "EXIST"
                              continue
                        else: print "NO EXISTE"
                        try:
                              princ = Mk()
                              print "pre mk text"
                              print str(url)
                              text = princ.monkey_learn_text_extract(url)
                              #text = unicode(text)
                              print [text]
                              #break
                              #sys.exit()
                        except:
                              print traceback.format_exc()
                              continue
                        try:
                              princ = Mk()
                              print "mk keyword"
                              #print [text]
                              if text:
                                    keyword = princ.monkey_learn_keyword_extract(text)
                                    
                                    if not keyword:
                                          print "\n"
                                          print " no keyword"
                                          print "\n" 
                                          continue
                              else:
                                    print "\n"
                                    print " no keyword"
                                    print "\n"
                                    continue
                        except:
                              print traceback.format_exc()
                              continue
                        #return text
                        print "pre save"
                        try:
                              s = SaveNews()
                              sav = s.saveme(
                                    title = title,
                                    subtitle = "",
                                    image = image,
                                    url = url,
                                    category = category,
                                    keyword = keyword,
                                    news_from = "la_republica",
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