from F import LIST

from F.LOG import Log
from FNLP.Language import Sentences
from FNLP.LanguageEngines import BaseModel
from FNLP.LanguageStructure.Variables import SentencesVariables


class SentencesManager(BaseModel, SentencesVariables):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def analyze_dates(self):
        for model in Log.ProgressBarYielder(self.input_models, prefix="Analyzing Sentences by Date..."):
            self.analyze_date(model)

    def analyze_date(self, model):
        content = self.get_content(model)
        date = self.get_date(model)
        temp_sentences = Sentences.to_sentences(str(content))
        temp_sentences_counted = len(temp_sentences)

        self.overall_sentences.append(temp_sentences)
        self.overall_sentences = LIST.flatten(self.overall_sentences)
        self.overall_sentences_counted = len(self.overall_sentences)

        wam = {"date": date, "sentences": temp_sentences, "sentences_counted": temp_sentences_counted}
        # Model
        if self.sentences_by_date.__contains__(date):
            temp_obj: list = self.sentences_by_date[date]
            temp_obj.append(wam)
            self.sentences_by_date[date] = temp_obj
        else:
            self.sentences_by_date[date] = [wam]
