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
           'Accept-Language': 'es-ES,en;q=0.8',
           'Connection': 'keep-alive'}

        #page = "http://www.lr21.com.uy/politica/1400838-astori-guerra-comercial-eeuu-china-economia-uruguaya"
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
        for line in stream:
            li=line
            print [li.encode("utf-8")]
            print " -- "
            #file2.write(line.rstrip().decode('utf8') + '\n')
            if not li.startswith("*"):
                if li.startswith("!") or li.startswith("\\"):pass
                else:
                    if li.startswith("#"): startWith = True
                    if li.startswith("#  !"): startWith = False
                    if li.startswith("###"): startWith = True
                    if startWith:
                        startWith = True
                        #print line.rstrip()
                        space += 1
                        #if (space == 10): break
                        #if not line.isspace():
                        if (li.startswith("FOTO") or 
    		        		li.startswith("Vota por esta noticia") or
    		        		li.startswith("Temas") or
    		        		li.startswith("Relacionadas") or
                            li.startswith("content") or 
                            li.startswith("-a") or
                            li.startswith("+A") or
                            li.startswith("Compartir esta noticia") or
                            li.startswith("  *   *   *   *   * __") or
                            li.startswith("SEGUIR") or 
                            li.startswith("Introduzca el texto aquí")

    		        	): pass
                        else:
                            if li.isspace:
                                space += 1
                            if space > 2 and "votos" in li: continue
                            if (li.startswith("NOTICIAS DE HOY") or 
                                li.startswith("EXPERIMENTO SOCIAL") or
                                li.startswith('Fuente') or
                                li.startswith("UyPress - ") or
                                li.startswith("jwl") or
                                li.startswith("Leer más sobre:") or
                                li.startswith("Comentarios:") or
                                li.startswith("RELACIONADAS") or 
                                li.startswith("Reportar error")
                            ): break
                            else: 
                                #print line.rstrip().decode('utf8') + '\n'
                                #print li
                                if li.isspace: s = s + li.decode('utf8') + "<br>"
                                else: s = s + li.decode('utf8')
                                #print s 
        #print s
        #text = re.sub('[#]', '', s)
        return s
        	
        	
    #print(text)




