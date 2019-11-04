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
from views.htmltotext.htmltotext3 import HtmlToTextMain

from save import SaveNews


class LaDiaria2(webapp2.RequestHandler):
      def get(self):
            try:
                  name = "/articulo/2015/9/la-construccion-de-mas-igualdad/"
                  url = "http://elmonoinfoarmado.appspot.com/la_diaria?name=/articulo/2015/9/la-construccion-de-mas-igualdad/"
                  #url = "http://charruanews.appspot.com/la_diaria"
                  #url = url + "?name=/articulo/2015/9/la-construccion-de-mas-igualdad/"
                  sock = urllib2.urlopen(url)
                  htmlSource = (sock.read()).decode("utf-8")
                  data = json.loads(htmlSource)
                  sock.close()   
                  soup = BeautifulSoup(htmlSource, "html.parser")
                  data = (soup.find_all("article"))[0]
                  
                  template = main.JINJA_ENVIRONMENT.get_template('/templates/json.html')
                  self.response.write(template.render(locals()))
            except:
                  print traceback.format_exc()
                  return traceback.format_exc()

class LaDiaria(webapp2.RequestHandler):
      def hack_la_diaria(self, url):
            try:
                  name = "/articulo/2015/9/la-construccion-de-mas-igualdad/"
                  url = "http://elmonoinfoarmado.appspot.com/la_diaria?name=/articulo/2015/9/la-construccion-de-mas-igualdad/"
                  #url = "http://charruanews.appspot.com/la_diaria"
                  #url = url + "?name=/articulo/2015/9/la-construccion-de-mas-igualdad/"
                  sock = urllib2.urlopen(url)
                  htmlSource = (sock.read()).decode("utf-8")
                  data = json.loads(htmlSource)
                  sock.close()   
                  soup = BeautifulSoup(htmlSource, "html.parser")
                  data = soup.find_all("article")
                  
                  template = main.JINJA_ENVIRONMENT.get_template('/templates/json.html')
                  self.response.write(template.render(locals()))
            except:
                  print traceback.format_exc()
                  return traceback.format_exc()

      def get(self):
            try:
                  page = "http://ladiaria.com.uy"
                  print "\n"
                  print "LaDiaria"
                  print "\n"
                  hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                        'Accept-Encoding': '*',
                        'Accept-Language': 'es-ES,en;q=0.8',
                        'Connection': 'keep-alive'
                  }
                  req = urllib2.Request(page, headers=hdr)
                  pageOpen = urllib2.urlopen(req)
                  content = pageOpen.read()
                  soup = BeautifulSoup(content, "html.parser")
                  def has_six_characters(css_class):
                        return css_class is not None and css_class in ["ld-card"]
                  url = soup.find_all(class_=has_six_characters)
                  c = 0; l = []
                  for i in url:
                        # img
                        try:
                              pre_url = (i.find_all("a"))[0]
                              url = pre_url["href"]
                              img = pre_url.img["data-srcset"]
                              img = img.split(",")[1].strip().split(" ")[0]
                              img = page + img
                              img = "<img class='lazy' src='" + img + "'>"
                              #print "\n"
                              #print url["href"]
                              #print "\n"
                        except:
                              try:
                                    img = pre_url.img["src"]
                                    #print img
                                    img = page + img
                                    img = "<img class='lazy' src='" + img + "'>"
                              except:
                                    print traceback.format_exc()
                                    from random import randint
                                    value = randint(0, 12)
                                    img = "<img class='lazy' src='img/lebo"+str(value)+".jpg'>"
                                    #break
                              
                              
                        try:
                              title = (i.find_all("h1"))[0].find_all("a")[0].text
                        except:
                              try:
                                    title = (i.find_all("h3"))[0].find_all("a")[0].text
                              except:
                                    try:
                                          title = (i.find_all("h4"))[0].find_all("a")[0].text
                                    except:
                                          print i
                                          print traceback.format_exc()
                                          title = ""
                                          break

                        
                        e = SaveNews()
                        e = e.if_exist(title, "la_diaria", c, url)
                        if e:
                              print "EXIST"
                              continue
                        else: print "NO EXISTE"
                        
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
                        
                        print "pre save"
                        try:
                              s = SaveNews()
                              sav = s.saveme(
                                    title = title,
                                    subtitle = "",
                                    image = img,
                                    url = url,
                                    category = "",
                                    keyword = [],
                                    news_from = "la_diaria",
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