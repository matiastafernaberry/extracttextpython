import sys
import traceback
from naiveBayesClassifier.ExceptionNotSeen import NotSeen


class TrainedData(object):
    def __init__(self):
        self.docCountOfClasses = {}
        self.frequencies = {}

    def increaseClass(self, className, byAmount = 1):
        self.docCountOfClasses[className] = self.docCountOfClasses.get(className, 0) + 1
        #print className

    def increaseToken(self, token, className, byAmount = 1):
        if not token in self.frequencies:
                self.frequencies[token] = {}

        self.frequencies[token][className] = self.frequencies[token].get(className, 0) + 1
        #print self.frequencies[token][className] 

    def decreaseToken(self, token, className, byAmount=1):
        if token not in self.frequencies:
            raise NotSeen(token)
        foundToken = self.frequencies[token]
        if className not in self.frequencies:
            sys.stderr.write("Warning: token %s has no entry for class %s. Not decreasing.\n" % (token, className))
            return
        if foundToken[className] < byAmount:
            raise ArithmeticError("Could not decrease %s/%s count (%i) by %i, "
                                  "as that would result in a negative number." % (
                                      token, className, foundToken[className], byAmount))
        foundToken[className] -= byAmount

    def getDocCount(self):
        """
        returns all documents count
        """
        return sum(self.docCountOfClasses.values())

    def getClasses(self):
        """
        returns the names of the available classes as list
        """
        return self.docCountOfClasses.keys()

    def getClassDocCount(self, className):
        """
        returns document count of the class. 
        If class is not available, it returns None
        """
        return self.docCountOfClasses.get(className, None)

    def getFrequency(self, token, className):
        try:
            from google.appengine.ext import ndb
            from models.models import Frequencies
            #e = Frequencies.query()
            #for i in e:
            #    i.key.delete()
                #print i.frequencies
            e = Frequencies.query(Frequencies.id == 1).get()
            if not e:
                s = Frequencies(
                    frequencies = self.frequencies,
                    id = 1,
                )
                s.put()
                #print s
            else:
                e.frequencies = self.frequencies
                e.put()
                #print e

            #print token
            e = Frequencies.query()
            for i in e:
                pass
                #print [i.frequencies['serlo']][0]["politica"]
                #print ""

            if token in self.frequencies:
                foundToken = self.frequencies[token]
                return foundToken.get(className)
            else:
                pass
                #raise NotSeen(token)
        except:
            print traceback.format_exc()

