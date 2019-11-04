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

from bs4 import BeautifulSoup



class Gsearch(webapp2.RequestHandler):
  def get(self):
    try:
      page = "https://www.google.com.uy/search?sclient=psy-ab&site=&source=hp&btnG=Buscar&q=uruguay"
      sock = urllib2.urlopen(page)
      htmlSource = sock.read()
      sock.close()
      soup = BeautifulSoup(htmlSource, "html.parser")
      url = soup.find_all("div",attrs={"class": "g"})
      print htmlSource
      for i in url:
        print i
      return url
    except: print traceback.format_exc()
        