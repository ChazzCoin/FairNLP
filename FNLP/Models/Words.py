import F.LIST
from F import LIST
from F.LOG import Log

from FNLP.Engines import Merge
from FNLP.Language import Words
from FNLP.Engines.Words import Analyzers
from FNLP.Models import BaseModel
from FNLP.Models.Variables import WordsVariables

class WordsEngine(BaseModel, WordsVariables):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def analyze_dates(self):
        for model in Log.ProgressBarYielder(self.input_models, prefix="Analyzing Words by Date..."):
            self.analyze_date(model)
    def analyze_date(self, model):
        content = self.get_content(model)
        date = self.get_date(model)
        # Results
        tokens = Words.to_words_v2(content)
        wam: WordsVariables = Analyzers.words_analyzer(tokens)

        temp_count = wam.overall_counts
        temp_tokens_counted = wam.overall_words_counted
        temp_unique_words = wam.unique_words
        temp_stop_count = wam.overall_stop_counts

        self.unique_words.append(temp_unique_words)
        uw = LIST.flatten_v2(self.unique_words)
        self.unique_words = F.LIST.remove_duplicates(uw)
        self.unique_words_counted = len(self.unique_words)

        self.overall_words_counted += temp_tokens_counted
        self.overall_counts = Merge.add_word_counts(temp_count, self.overall_counts)
        self.overall_stop_counts = Merge.add_word_counts(temp_stop_count, self.overall_stop_counts)
        # Model
        if self.overall_words_by_date.__contains__(date):
            temp_obj: list = self.overall_words_by_date[date]
            temp_obj.append(wam)
            self.overall_words_by_date[date] = temp_obj
        else:
            self.overall_words_by_date[date] = [wam]
