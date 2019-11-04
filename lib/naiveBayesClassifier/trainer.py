from naiveBayesClassifier.trainedData import TrainedData

class Trainer(object):

    """docstring for Trainer"""
    def __init__(self, tokenizer):
        super(Trainer, self).__init__()
        #print dir(tokenizer)
        self.tokenizer = tokenizer
        self.data = TrainedData()
        #print dir(self.data)

    def train(self, text, className):
        """
        enhances trained data using the given text and class
        """
        self.data.increaseClass(className)

        tokens = self.tokenizer.tokenize(text)
        #print tokens
        a = []
        for token in tokens:
            #print "previo: " + token
            #token = token.strip()
            token = self.tokenizer.remove_stop_words(token)
            token = self.tokenizer.remove_punctuation(token)
            
            if (token != "stopword"):
                #print token
                a.append(token)

                self.data.increaseToken(token, className)

        print a
