from F.LOG import Log
from FNLP.Language import Paragraphs
from FNLP.LanguageEngines import BaseModel
from FNLP.LanguageStructure.Variables import ParagraphsVariables

"""
word = name of word
count = number of times this word has been seen
score = algo for giving a word a score (seen, 

"""

class ParagraphsManager(BaseModel, ParagraphsVariables):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run_analyzer(self):
        self.paragraphs = Paragraphs.to_paragraphs(self.input_p_content)
        self.paragraph_count = len(self.paragraphs)

    def analyze_dates(self):
        for model in Log.ProgressBarYielder(self.input_models, prefix="Analyzing Words by Date..."):
            self.analyze_date(model)

    def analyze_date(self, model):
        content = self.get_content(model)
        date = self.get_date(model)
        self.paragraphs = Paragraphs.to_paragraphs(content)
        self.paragraph_count = len(self.paragraphs)