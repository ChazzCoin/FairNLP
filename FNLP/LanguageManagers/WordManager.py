from F.CLASS import FairClass
from FNLP.LanguageEngines.Words import Analyzers
from FNLP.LanguageStructure.Variables import WordVariables

class WordManager(FairClass, WordVariables):

    def __init__(self, word, **kwargs):
        super().__init__(**kwargs)
        self.word = word
        self.run_analyzer()

    def run_analyzer(self):
        breakdown = Analyzers.analyze_word(self.word)
        self.fromJson(breakdown)
        return breakdown

    def import_model(self, model: dict):
        """ Load JSON Model """
        self.fromJson(model)

    def export_model(self):
        """ Export Model as JSON"""
        return self.toJson(removeNone=True)

    def print_model(self):
        print(self.toJson())