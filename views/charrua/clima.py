# -*- coding: utf-8 -*-
import webapp2
import jinja2
import traceback
import urllib, urllib2
import httplib
import time
from datetime import date,datetime

from models.models import NewsSelect

from datetime import date
from bs4 import BeautifulSoup



class Yahoo(webapp2.RequestHandler):
    def get(self):
        def dias(dia):
            if dia == "Thu": dia = "Jueves"
            elif dia == "Fri": dia = "Viernes"
            elif dia == "Sat": dia = "Sabado"
            elif dia == "Sun": dia = "Domingo"
            elif dia == "Mon": dia = "Lunes"
            elif dia == "Tue": dia = "Martes"
            elif dia == "Wed": dia = "Miercoles"
            return dia

        def fecha(f):
            f = str(f)
            if 'Jan' in f: f = f.replace("Jan","Enero")
            if 'Feb' in f: f = f.replace("Feb","Febrero")
            if 'Mar' in f: f = f.replace("Mar","Marzo")
            if 'Apr' in f: f = f.replace("Apr","Abril")
            if 'May' in f: f = f.replace("May","Mayo")
            if 'Jun' in f: f = f.replace("Jun","Junio")
            if 'Jul' in f: f = f.replace("Jul","Julio")
            if 'Aug' in f: f = f.replace("Aug","Agosto")
            if 'Sept' in f: f = f.replace("Sept","Septiembre")
            if 'Oct' in f: f = f.replace("Oct","Octubre")
            if 'Nov' in f: f = f.replace("Nov","Noviembre")
            if 'Dec' in f: f = f.replace("Dec","Diciembre")
            return f
        # pasa de fahrenheit a celsius
        def fah_cel(f):
            c = (int(f) - 32) * 5/9
            return c

        url = 'https://api.login.yahoo.com/oauth2/get_token'
        import urllib2, urllib, json
        baseurl = "https://query.yahooapis.com/v1/public/yql?"
        yql_query = "select * from weather.forecast where woeid=468052"
        yql_url = baseurl + urllib.urlencode({'q':yql_query,'u':'c'}) + "&format=json"
        data = urllib2.urlopen(yql_url).read()
        data = json.loads(data)
        # data.query.results.channel.item.forecast
        # (73 - 32) * 5.0/9.0
        l = ['Tornado','Tormenta Tropical','Huracán',
        'Tormentas Eléctricas Severas','Tormentas Eléctricas',
        'Lluvia y Nieve','Lluvia y Aguanieve','Nieve y Aguanieve',
        'Llovizna congelada','Llovizna','Lluvia congelada',
        'Lluvia','Lluvia','Ráfagas de Nieve','Nevada ligera',
        'Nieve con viento','Nieve','Granizo','Aguanieve',
        'Polvo','Neblina','Niebla ligera','Neblina',
        'Vendaval','Con viento','Helado','Nublado',
        'Muy nublado (noche)','Muy nublado (dia)',
        'Parcialmente nublado (noche)',
        'Parcialmente nublado (dia)',
        'Despejado (noche)','Soleado','Despejado (noche)',
        'Despejado (dia)','Lluvia y Granizo','Caluroso',
        'Tormentas eléctricas aisladas',
        'Tormentas eléctricas dispersas',
        'Tormentas eléctricas dispersas',
        'Lluvia dispersa','Nieve densa','Nieve y lluvia dispersas',
        'Nieve densa','Parcialmente nublado',
        'Tormentas eléctricas','Nieve',
        'Tormentas eléctricas aisladas',
        'No disponible']


        #print data['query']['results']['channel']['item']['forecast']
        tiempo = data['query']['results']['channel']['item']['forecast']
        show = []
        for i in tiempo:
            d = {}
            low = fah_cel(i['low'])
            d["low"] = low
            high = fah_cel(i['high'])
            d["high"] = high
            code = i['code']
            d["code"] = code
            d["image"] = l[int(code)]
            day = i['day']
            d["day"] = dias(day)
            date = i['date']
            date = fecha(date)
            date = date.replace(" 2017","")
            d["date"] = date
            #text = i['text']
            show.append(d)
            #print d

        return show

class Clima(webapp2.RequestHandler):
    def get(self):
        try:
            # clima
            try:
                def dias(dia):
                    if dia == "Thu": dia = "Jueves"
                    elif dia == "Fri": dia = "Viernes"
                    elif dia == "Sat": dia = "Sabado"
                    elif dia == "Sun": dia = "Domingo"
                    elif dia == "Mon": dia = "Lunes"
                    elif dia == "Tue": dia = "Martes"
                    elif dia == "Wed": dia = "Miercoles"
                    return dia

                def mes_string(mes):
                    if mes == "09": mes = "Septiembre"
                    if mes == "10": mes = "Octubre"
                    return mes

                #468052

                pagina = "https://api.login.yahoo.com/oauth2/request_auth?client_id=dj0yJmk9TTVBYXdmYUlsVTlNJmQ9WVdrOVdIQnFaekZtTjJrbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD0wOQ--&response_type=id_token&redirect_uri=http://charruanews.appspot.com/googlea6bed3b812c0e8c8&scope=openid%20mail-r&nonce=YihsFwGKgt3KJUh6tPs2"

                sock = urllib.urlopen(pagina)
                htmlSource = sock.read()
                sock.close()   
                soup = BeautifulSoup(htmlSource, "html.parser")
                print soup
                # return True
                # temperatura = (soup.find("yweather:condition").get("temp"))
                # fecha = unicode(soup.find("yweather:forecast").get("date"))[:2]
                # icono = (soup.find("yweather:condition").get("code"))
                # l = ['Tornado','Tormenta Tropical','Huracán',
                #     'Tormentas Eléctricas Severas','Tormentas Eléctricas',
                #     'Lluvia y Nieve','Lluvia y Aguanieve','Nieve y Aguanieve',
                #     'Llovizna congelada','Llovizna','Lluvia congelada',
                #     'Lluvia','Lluvia','Ráfagas de Nieve','Nevada ligera',
                #     'Nieve con viento','Nieve','Granizo','Aguanieve',
                #     'Polvo','Neblina','Niebla ligera','Neblina',
                #     'Vendaval','Con viento','Helado','Nublado',
                #     'Muy nublado (noche)','Muy nublado (dia)',
                #     'Parcialmente nublado (noche)',
                #     'Parcialmente nublado (dia)',
                #     'Despejado (noche)','Soleado','Despejado (noche)',
                #     'Despejado (dia)','Lluvia y Granizo','Caluroso',
                #     'Tormentas eléctricas aisladas',
                #     'Tormentas eléctricas dispersas',
                #     'Tormentas eléctricas dispersas',
                #     'Lluvia dispersa','Nieve densa','Nieve y lluvia dispersas',
                #     'Nieve densa','Parcialmente nublado',
                #     'Tormentas eléctricas','Nieve',
                #     'Tormentas eléctricas aisladas',
                #     'No disponible']
                # descripcion = (l[int(icono)]).decode("utf-8")
                # max = soup.find("yweather:forecast").get("high")
                # min = soup.find("yweather:forecast").get("low")
                # #sensacion = soup.find("aws:feels-like").get_text()
                # humedad = soup.find("yweather:atmosphere").get("humidity")
                # viento = soup.find("yweather:wind").get("speed")
                # dia = soup.find("yweather:forecast").get("day")
                # dia = dias(dia)
                
                # dia_2 = soup.find_all("yweather:forecast")[1]
                # dia2 = dia_2.get("day")
                # dia2 = dias(dia2)
                # icono2 = dia_2.get("code")
                # descripcion2 = (l[int(icono2)]).decode("utf-8")
                # max2 = dia_2.get("high")
                # min2 = dia_2.get("low")
                # fecha2 = unicode(dia_2.get("date"))[:2]
                
                # dia_3 = soup.find_all("yweather:forecast")[2]
                # dia3 = dia_3.get("day")
                # dia3 = dias(dia3)
                # icono3 = dia_3.get("code")
                # descripcion3 = (l[int(icono3)]).decode("utf-8")
                # max3 = dia_3.get("high")
                # min3 = dia_3.get("low")
                # fecha3 = unicode(dia_3.get("date"))[:2]
                
                # dia_4 = soup.find_all("yweather:forecast")[3]
                # dia4 = dia_4.get("day")
                # dia4 = dias(dia4)
                # icono4 = dia_4.get("code")
                # descripcion4 = (l[int(icono4)]).decode("utf-8")
                # max4 = dia_4.get("high")
                # min4 = dia_4.get("low")
                # fecha4 = unicode(dia_4.get("date"))[:2]
                # try:
                #     dia_5 = soup.find_all("yweather:forecast")[4]
                #     dia5 = dia_5.get("day")
                #     dia5 = dias(dia5)
                #     icono5 = dia_5.get("code")
                #     descripcion5 = (l[int(icono5)]).decode("utf-8")
                #     max5 = dia_5.get("high")
                #     min5 = dia_5.get("low")
                #     fecha5 = unicode(dia_5.get("date"))[:2]
                # except: pass

                # hoy = date.today()
                # last = NewsSelect.query(
                #     NewsSelect.date == hoy,
                # ).order(-NewsSelect.id).get()
                # try:
                #     update = last.created
                # except AttributeError:
                #     last = NewsSelect.query().order(-NewsSelect.id).get()
                #     update = last.created

                # dia = update.strftime('%d')
                # fecha= update.strftime('%m')
                # mes = mes_string(fecha)
                # year= update.strftime('%Y')

                # day_week_string = dias(dia)
                # ahora_datetime = datetime.today()
                # dayweek_string = ahora_datetime.strftime("%a")
                # diasemana_string = dias(dayweek_string)

            except: 
                print traceback.format_exc() 
                return False
            hoy = date.today()
            
            return locals()
        except:
            print traceback.format_exc()
            return False
            