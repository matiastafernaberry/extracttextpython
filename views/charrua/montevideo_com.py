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

from bs4 import BeautifulSoup
from save import SaveNews
from models.models import News


class MontevideoCom(webapp2.RequestHandler):
    def get(self):
        try:
            page = "http://www.montevideo.com.uy/index.html"
            sock = urllib2.urlopen(page)
            htmlSource = sock.read()
            sock.close()   
            soup = BeautifulSoup(htmlSource, "html.parser")
            # PORTADA
            portada = soup.find_all("article")
            #print ""
            #print portada[1]
            #return True
            #portada = portada[0].find_all("div", attrs={"id": re.compile("^uc")})
            t = [] 
            c = 0
            for i in portada:
                ### image ###
                try:
                    image = i.find_all("img")[0]
                    image = str(image).replace("data-src","src")
                    image = str(image)
                    image = image[:5] + "class='img-responsive'" + image[4:]
                    #image = BeautifulSoup(image, "html.parser")
                    #print ""
                    #print image
                    #print "" 
                except:
                    print traceback.format_exc()
                    
                ### tag ###
                try:
                    tag = i.find_all("h3")[0].string
                    #print [tag]
                    #print ""
                except:
                    tag = ""
                    print traceback.format_exc()

                ### title ###
                try:
                    title = i.find_all("h2")[0].string
                    #print [title]
                except:
                    title = ""
                    print traceback.format_exc()

                ### subtitle ###
                try:
                    subtitle = i.find_all("p")[0].string
                    #print [subtitle]
                    #print ""
                except:
                    subtitle = ""
                    print traceback.format_exc()

                ### url ###
                try:
                    url = i.find_all("a")[0]["href"]
                    print [url]
                    if "futbol" in str(url):
                        tag = "deportes"
                    print ""
                except:
                    url = ""
                    print traceback.format_exc()

                # check if exist in database
                e = SaveNews()
                e = e.if_exist(title, "montevideo_com", c, url)
                if e:
                  print "Existe"
                  c = c + 1
                  time.sleep(1) 
                  continue

                # TEXT EXTRACT
                try:
                    print "TEXT EXTRACT"
                    print url
                    text = HtmlToTextMain()
                    text = text.main(url)
                    #print text
                    #if c == 4: break
                except:
                    print traceback.format_exc()
                    continue
                # KEYWORD EXTRACT

                print "PRE SAVE"
                
                try:
                    s = SaveNews()
                    sav = s.saveme(
                        news_from = "montevideo_com",
                        title = title,
                        subtitle = subtitle,
                        image = image,
                        url = url,
                        category = tag,
                        keyword = [],
                        id = c,
                        html = text,
                    )
                except: 
                    print traceback.format_exc()
                    continue
                print "SAVE"
                

                c += 1
                print c
                print "SLEEP"
                time.sleep(2)
                print "WAKE UP"
                

        except:
            print traceback.format_exc() 
            return traceback.format_exc()


