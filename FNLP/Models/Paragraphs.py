from FNLP.Language import Paragraphs
from FNLP.Models import BaseModel
from FNLP.Models.Variables import ParagraphVariables

"""
word = name of word
count = number of times this word has been seen
score = algo for giving a word a score (seen, 

"""

class ParagraphsModel(BaseModel, ParagraphVariables):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run_analyzer(self):
        self.paragraphs = Paragraphs.to_paragraphs(self.input_p_content)
        self.paragraph_count = len(self.paragraphs)

    def import_model(self, model: dict):
        """ Load JSON Model """
        self.fromJson(model)

    def export_model(self):
        """ Export Model as JSON"""
        return self.toJson(removeNone=True)

    def print_model(self):
        print(self.toJson())