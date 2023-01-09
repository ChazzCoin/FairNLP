from FNLP.Language import Sentences
from FNLP.Models import BaseModel
from FNLP.Models.Variables import SentenceVariables


class SentencesModel(BaseModel, SentenceVariables):

    def __init__(self, input_s_raw, **kwargs):
        super().__init__(**kwargs)
        self.input_s_raw = input_s_raw

    def run_analyzer(self):
        self.sentences = Sentences.to_sentences(self.input_s_raw)
        self.sentence_count = len(self.sentences)
        pass
