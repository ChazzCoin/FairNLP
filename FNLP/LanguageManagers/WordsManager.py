import F.LIST
from F import LIST
from F.LOG import Log

from FNLP import Merge
from FNLP.Language import Words
from FNLP.LanguageEngines.Words import Analyzers
from FNLP.LanguageStructure.Variables import WordsVariables

class WordsManager(WordsVariables):
    """
    -> Organizes words analyzed by Date of webpage/content.
        overall_words_by_date       = { "_id": datetime, "word_counts": { "ALL_WORDS": count }, "words_counted": XX }
        stop_words_by_date          = { "_id": datetime, "word_counts": { "FILTERED_WORDS": count }, "words_counted": XX }

    -> Raw overall memory of words and how many times we've counted that word.
        overall_counts: dict        = { "ALL_WORDS": count }
        overall_words_counted: int  = 0
        overall_stop_counts: dict   = { "FILTERED_WORDS": count }

    -> Organizing Unique words looked at/counted.
        unique_words: list          = ["word1", "word2] -> No duplicate words.
        unique_words_counted: int   = XX -> Count of unique words.
    """

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
            temp_obj: WordsManager = self.overall_words_by_date[date]
            temp_obj.absorb_model(wam)
            self.overall_words_by_date[date] = temp_obj
        else:
            self.overall_words_by_date[date] = wam
