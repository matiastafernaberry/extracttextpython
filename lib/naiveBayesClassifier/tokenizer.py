# -*- coding: utf-8 -*-
import re

class Tokenizer(object):
    def __init__(self, stop_words = [], signs_to_remove = ["?!#%&."]):
        self.stop_words = stop_words
        self.signs_to_remove = signs_to_remove

    def tokenize(self,text):
        #print "tokenize"
        return text.lower().split()

    def remove_stop_words(self,token):
        #print "remove_stop_words"

        if token in self.stop_words:
            #print "stop_word"
            return "stop_word"
        else:
            return token

    def remove_punctuation(self,token):
        #print "remove_punctuation"
        token = re.sub(r'\W+',"",token)
        return re.sub(str(self.signs_to_remove),"",token)
