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
from save import SaveNews
from monkeylearn import Mk




class Teledoce(webapp2.RequestHandler):
    def get(self):
        try:
            # manejar error HTTP
            error = []
            page = "http://www.teledoce.com/"
            sock = urllib2.urlopen(page)
            htmlSource = sock.read()
            sock.close()   
            soup = BeautifulSoup(htmlSource, "html.parser")
            url = soup.find_all("article",attrs={"class": "item"})
            l = []; c = 0
            #f = News.query()
            #return "ho"
            for u in url: 
                if u:
                    # TITLE
                    if (u.find_all("h2", attrs={"class": "title"})):
                        title = u.find_all("h2", attrs={"class": "title"})
                        if title: 
                            title = title[0]
                            title = title.a.string
                        else:
                            print "no title"
                    if (u.find_all("h1", attrs={"class": "title"})):
                        title = u.find_all("h1", attrs={"class": "title"})
                        if title: 
                            title = title[0]
                            title = title.a.string
                        else:
                            print "no title"
                    if (u.find_all("h3", attrs={"class": "title"})):
                        title = u.find_all("h3", attrs={"class": "title"})
                        if title: 
                            title = title[0]
                            title = title.a.string
                        else:
                            print "no title"

                    # check if exist in database
                    e = SaveNews()
                    e = e.if_exist(title, "el_observador")
                    if e: continue

                    # IMAGE
                    try:
                        image = (u.find_all("img"))[0]
                        src = image["src"]

                        if ".." in str(image): 
                            image = str(image)
                            image = image.replace("..","//static.elobservador.com.uy")
                        image = "<img src='" + src + "' />"

                        url = (u.find_all("a"))[0]
                        url = url["href"]
                        if "http:" in str(url):
                            url = str(url)
                        else:
                            url = "http:" + url
                    except httplib.HTTPException:
                        print "HTTPException"
                        print "sleep"
                        time.sleep(2)
                    except: 
                        print image
                        print traceback.format_exc()
                        continue
                    
                    #print image

                    # TEXT EXTRACT

                    try:
                        te = Mk()
                        if url:
                            text = te.monkey_learn_text_extract(url)
                        else: continue
                        print "ok mk text"
                        #print [text]
                    except: 
                        print traceback.format_exc()
                        continue
                        return traceback.format_exc()

                    # KEYWORD EXTRACT
                    k = []
                    try:
                        ke = Mk()
                        print "pre mk key"
                        keyword = ke.monkey_learn_keyword_extract(text)
                        print keyword
                        if not keyword: continue
                    except: 
                        print traceback.format_exc()
                        continue
                        
                    
                    # data
                    #return u
                    subtitle = u.find_all("p", attrs={"class": "preview"})
                    if subtitle: 
                        try:
                            subtitle = (subtitle[0]).find_all("span")[1]
                            subtitle = subtitle.string
                        except: 
                            subtitle = (subtitle[0]).find_all("a")[1]
                            subtitle = subtitle.string
                    

                    category = u.find_all("span", attrs={"class": "category"})
                    if category: 
                        category = category[0]
                        category = category.string
                    

                    savemi = SaveNews()
                    print "pre save"
                    save = savemi.saveme(
                        title = title, 
                        subtitle = subtitle, 
                        image = image,
                        url = url,
                        category = category,
                        keyword = keyword,
                        news_from = "el_observador",
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
            #return error

            return True
        #except httplib.HTTPException: 
        #    princ = Charrua()
        #    elobservador = princ.elobservador()
        except: 
            print traceback.format_exc()
            return False