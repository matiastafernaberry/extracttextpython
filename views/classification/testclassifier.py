# -*- coding: utf-8 -*-
import webapp2
import jinja2
import traceback
"""
Suppose you have some texts of news and know their categories.
You want to train a system with this pre-categorized/pre-classified 
texts. So, you have better call this data your training set.
"""
from models.models import News3
from datetime import date

from naiveBayesClassifier import tokenizer
from naiveBayesClassifier.trainer import Trainer
from naiveBayesClassifier.classifier import Classifier

class TestClassifier(webapp2.RequestHandler):
	''' '''
	def get(self):
		try:
			print "  "
			print "TestClassifier start"
			print "  "
			# pasar  los stop words a lista desde el file
			with open("stop_words.txt", "r") as ins:
				array = []
				for line in ins:
					array.append((line.rstrip('\n')).decode('unicode-escape'))
			#print array
			newsTrainer = Trainer(tokenizer.Tokenizer(stop_words = array, signs_to_remove = ["?!#%&_"]))

			hoy = date.today()

			query = News3.query(
				News3.date == hoy,
				News3.news_from.IN([
                    "uy_press",
                ]),
                News3.category == "Política"
            )

			# You need to train the system passing each text one by one to the trainer module.
			#newsSet =[
			#    {'text': 'not to eat too much is not enough to lose weight', 'category': 'health'},
			#    {'text': 'Russia try to invade Ukraine', 'category': 'politics'},
			#    {'text': 'do not neglect exercise', 'category': 'health'},
			#    {'text': 'Syria is the main issue, Obama says', 'category': 'politics'},
			#    {'text': 'eat to lose weight', 'category': 'health'},
			#    {'text': 'you should not eat much', 'category': 'health'}
			#]

			query2 = News3.query(News3.date == hoy,News3.news_from == "uy_press",News3.category == "deportes")

			query4 = News3.query(News3.date == hoy,News3.news_from == "uy_press",News3.category == "salud")

			#for news in newsSet:
			#    newsTrainer.train(news['text'], news['category'])
			c = 0
			#print query
			for i in query:
				print "  "
				print i.category
				newsTrainer.train(i.html, 'politica')
				#if c == 10: break
				c += 1

			#for i in query2:
			#	newsTrainer.train(i.html, 'deportes')
			#raise Exception('I know Python!')

			#for i in query4:
			#	newsTrainer.train(i.html, 'salud')
			    
			# When you have sufficient trained data, you are almost done and can start to use
			# a classifier.
			

			# Now you have a classifier which can give a try to classifiy text of news whose
			# category is unknown, yet.
			query3 = News3.query(
		    	News3.date == hoy,
                News3.news_from.IN([
                    "el_pais",
                ]),
                News3.id.IN([0]),
            )

			###
			newsClassifier = Classifier(newsTrainer.data, tokenizer.Tokenizer(stop_words = array, signs_to_remove = ["?!#%&"]))
			#print unknownInstance
			classification = newsClassifier.classify("Vidalín: No quiero que me llamen para saber qué tramite hay que hacer para poner un prostíbulo")

			# the classification variable holds the detected categories sorted
			print " classification "
			print(classification)
		except:
			print traceback.format_exc()
