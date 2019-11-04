#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import cgi
import os
import re
import json
import webapp2
import jinja2
import traceback
import urllib, urllib2

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import ndb
import webapp2

from webapp2_extras import sessions

from models import Films
from bs4 import BeautifulSoup


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True,
    )

class Main(webapp2.RequestHandler):
    '''  '''
    def grupocine(self):
        try:
            page = "http://www.grupocine.com.uy/categoria_15_1.html"
            sock = urllib.urlopen(page)
            htmlSource = sock.read()
            sock.close()   
            soup = BeautifulSoup(htmlSource, "html.parser")
            image = soup.find_all('img',src=re.compile("imgnoticias"))
            title = (soup.find_all(attrs={"class": "contenidoUCh3"}))
            tittle = []
            for i in title: tittle.append(i.string)
            shedule = soup.find_all(attrs={"class": "contenidoUCh4"})
            description = soup.find_all(attrs={"class": "contenidoUCh5"})
            f = []
            for i,j,k,l in zip(tittle, shedule, description, image):
                if False: #Films.query(Films.title == i.encode('utf8', 'replace')):
                    #edit = Films.query(Films.title == i.encode('utf8', 'replace'))
                    edit_key = (ndb.Key("Films", i.encode('utf8', 'replace'))).urlsafe()
                    edit_key2 = Films.query(Films.title == i.encode('utf8', 'replace'))
                    edit = edit_key2.get()
                    list_cine = edit.cine
                    edit.cine.append("life")
                    edit.put()
                    return edit
                else: #f.append((i,j,k,l))
                    save = Films(
                        title = i.encode('utf8', 'replace'), 
                        shedule = str(j),
                        description = str(k),
                        image = str(l),
                        cine = ["grupocine"]
                    )
                    save.put()
            f = Films.query()
            return f
        except: return traceback.format_exc()

    def movie(self):
        try:
            page = "http://www.movie.com.uy/cine/"
            sock = urllib.urlopen(page)
            htmlSource = sock.read()
            sock.close()   
            soup = BeautifulSoup(htmlSource, "html.parser")
            tittle = []
            # extract tittle
            for i in (soup.find_all("div", "hd")):
                if i.a: tittle.append(i.a.string) 
            # extract foto
            foto = []
            for i in (soup.find_all(src=re.compile("afiche"))):
                foto.append(i) 
            
            return foto
        except: return traceback.format_exc()

    def get(self):
    	#pagina = "http://weather.yahooapis.com/forecastrss?p=UYXX0006&u=c"
        princ = Main()
        grupoc = princ.grupocine()
        #movi = princ.movie()

        template_values = {
            'grupoc': grupoc,
        }
        template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        self.response.write(template.render(template_values))


class PedidosYaLogin(webapp2.RequestHandler):
    '''  '''
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)
        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()
        
    def get(self):
        token = self.session.get('token')
        if token:
            template_values = {
                'hola': token,
            }
            template = JINJA_ENVIRONMENT.get_template('templates/pedidoya.html')
            self.response.write(template.render(template_values))
        else: self.redirect("/pedidosya")


class PedidosYa(webapp2.RequestHandler):
    '''  '''
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)
        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

    def get(self):
        template_values = {
            'hola': "hola",
        }
        template = JINJA_ENVIRONMENT.get_template('templates/pedidoyalogin.html')
        self.response.write(template.render(template_values))

    def post(self):
        page = "http://stg-api.pedidosya.com/public/v1/tokens?clientId=test&clientSecret=PeY@@Tr1v1@943"
        sock = urllib.urlopen(page)
        htmlSource = sock.read()
        sock.close()
        data = json.loads(htmlSource)
        token = data['access_token']
        error = False
        try:
            email = self.request.get('email')
            password = self.request.get('pass')
            site = "http://stg-api.pedidosya.com/public/v1/tokens?userName=%s&password=%s" % (email, password)
            req = urllib2.Request(site)
            req.add_header('Authorization', token)
            sock2 = urllib2.urlopen(req)
            data = sock2.read()
            sock2.close()
            data = json.loads(data)
            token2 = data['access_token']
            self.session['token'] = token2
        except urllib2.HTTPError, e: 
            error = True# e.fp.read()

        if error:
            template = JINJA_ENVIRONMENT.get_template('templates/401.html')
            self.response.write(template.render())
        else:
            template_values = {
                'email': token2,
                'pass': password,
            }
            self.redirect("/login")
            #template = JINJA_ENVIRONMENT.get_template('templates/pedidoya.html')
            #self.response.write(template.render(template_values))

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}

app = webapp2.WSGIApplication([
    ('/', Main),
    ('/pedidosya', PedidosYa),
    ('/login', PedidosYaLogin),
], config=config, debug=True)


def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()
