from FNLP.Language import Words
from FNLP.Engines.Words import Analyzers
from FNLP.Models import BaseModel
from FNLP.Models.Variables import WordsVariables

class WordsModel(BaseModel, WordsVariables):

    def __init__(self, input_content, **kwargs):
        super().__init__(**kwargs)
        self.input_content = input_content
        self.input_tokens = Words.to_words_v2(self.input_content)

    def run_analyzer(self):
        breakdown = Analyzers.words_analyzer(self.input_tokens)
        self.fromJson(breakdown)
        return breakdown
