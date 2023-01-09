from F.DATE import TODAY
from F.LOG import Log
from FM.QueryHelper import O
from FNLP.Language import Words

from F import DATE, CONVERT, DICT, LIST
from FNLP.Models import BaseModel
from FNLP.Models.Paragraphs import ParagraphsModel
from FNLP.Models.Sentences import SentencesModel
from FNLP.Models.Variables import ContentVariables, BaseVariables
from FNLP.Models.Words import WordsModel
Log = Log("ContentModel")


class ContentModel(BaseModel, BaseVariables, ContentVariables):
    """ VARIABLES ARE IN 'CONTENTVARIABLES' UNDER VARIABLES MODEL """

    def run_analyzer(self):
        self.model_words = WordsModel(input_content=self.input_contents)
        self.model_words.run_analyzer()
        self.model_sentences = SentencesModel(input_s_raw=self.input_main_content_only)
        self.model_sentences.run_analyzer()
        # self.model_paragraphs = ParagraphsModel(input_p_content=self.input_contents).run_analyzer()
        # self.model_paragraphs.run_analyzer()

    def add_webpages(self, webpages:list):
        for ac in Log.ProgressBarYielder(webpages, prefix="Preparing Content..."):
            self.add_webpage(ac)

    def add_webpage(self, webpage:dict):
        # Internal for The Brain
        id = DICT.get("_id", webpage, default="Unknown")
        new_date = DICT.get("pub_date", webpage, None)
        model = { "_id": O.TO_OBJECT_ID(id), "webpage_date": new_date, "updatedDate": TODAY }
        self._webpage_models.append(model)
        # Extract Values only from Dict/Obj
        new_content = CONVERT.dict_TO_List_OF_Values(webpage)
        self.input_contents.append(new_content)
        # Create and Add Tokens
        new_tokens = Words.to_words_v2(str(new_content))
        self.input_tokens_by_content.append(new_tokens)
        # Add Date
        if new_date:
            self._dates_analyzed.append(new_date)
        # Category Scores
        # cat_scores = DICT.get("category_scores", webpage, None)
        # if cat_scores:
        #     self.category_scores = DICT.add_word_count(self.category_scores, cat_scores)
        title = DICT.get("title", webpage, "")
        body = DICT.get("body", webpage, "")
        self.input_main_content_only = self.input_main_content_only + " " + str(title) + " " + str(body)
        self.post_add_webpage_work()

    def post_add_webpage_work(self):
        self.input_tokens = LIST.flatten(self.input_tokens_by_content)
        self._dates_analyzed = LIST.remove_duplicates(self._dates_analyzed)
        self._dates_analyzed_count = len(self._dates_analyzed)
        self._webpages_analyzed_count = len(self.input_contents)




















































