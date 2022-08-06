import F

from FNLP.Language import Words


class Sentence:
    id = F.get_uuid()
    rawText = ""
    orderNumber = None
    words = []

    def __init__(self, text, orderNumber=None):
        self.rawText = text
        self.orderNumber = orderNumber
        self.words = []

    def tokenize(self):
        self.words = Words.to_words_v1(self.rawText)
        return self.words

class Sentences:
    sentences: [Sentence]


"""

 0: { 
     0: "Sentence()",
     1: "sentence2",
     2: "sentence3",
     3: "sentence4",
     4: "sentence5"
    }
    
    
"""