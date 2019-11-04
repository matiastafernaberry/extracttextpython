# -*- coding: utf-8 -*-
import webapp2
import jinja2
import traceback
import time
import urllib, urllib2
import re

from bs4 import BeautifulSoup
from google.appengine.ext.webapp import template
import webapp2
from models.models import News
#from elpais import Elpais
from montevideo_com import MontevideoCom
#from elobservador import ElObservador
#from ciento_ochenta import CientoOchenta



