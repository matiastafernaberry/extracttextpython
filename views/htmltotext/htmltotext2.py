# -*- coding: utf-8 -*-
import html2text
import urllib, urllib2, re
import codecs
import webapp2
import StringIO
import jinja2
import traceback
import urllib, urllib2
import httplib
import time, os


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__).replace("views/otrosine","")),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True,
)


class HtmlToTextMain(webapp2.RequestHandler):
    ''' '''
    def init(self):
        page = "http://www.elpais.com.uy/informacion/lacalle-guerrilla-tupamara-provoco-dictadura.html"
        o = main(page)

        template_values = {
            'data2': o,
            
        }
        template = JINJA_ENVIRONMENT.get_template('/templates/mono2.html')
        self.response.write(template.render(template_values))

    def main(self, page):
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': '*',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

        req = urllib2.Request(page, headers=hdr)
        page = urllib2.urlopen(req)
        content = page.read()

        #text = html2text.html2text(content.decode('utf8'))
        #pdb.set_trace()
        text = html2text.HTML2Text()
        text.lastWasList = True
        text.ignore_links = True
        text.skip_internal_links = True
        text.escape_snob = True
        text.re_space = True
        text.escape_all = True
        text.re_ordered_list_matcher = True
        text.re_unordered_list_matcher = True
        text.store_true = True
        text.list_indent = True

        try:
            text = text.handle(content.decode('utf8'))
        except UnicodeDecodeError:
            text = text.handle(content.decode("ISO-8859-1"))

        output = StringIO.StringIO()
        output.write(text)
        contents = output.getvalue()
        output.close()
        startWith = False
        space = 0
        def string_stream(s, separators="\n"):
            start = 0
            for end in range(len(s)):
                if s[end] in separators:
                    yield s[start:end]
                    start = end + 1
            if start < end:
                yield s[start:end+1]
                #print text
        stream = string_stream(contents)
        s = ""
        def createString(texto):
            pass

        
        for li in stream:
            startWith = True
            li = li.strip()
            if (li.startswith("*")): continue
            if (li.startswith("__")): continue
            if (li.startswith(" ")): continue
            if (li.startswith("!")): continue
            if (li.startswith("\\")): continue
            if (li.startswith("#  !")): continue
            if (li.startswith("EL PAIS Información")): continue
            #if (li.isspace): continue
            #print li
            #else: startWith = True
            if (True):
                #print " ******************************* "
                if (li.isspace): 
                    print "true"
                    continue
                print li
                s = s + li.decode('utf8') + '\n'
                space += 1
                if space == 20: break
                startWith = False
        #print s
        text = re.sub('[#]', '', s)
        return text    
        #print(text)




