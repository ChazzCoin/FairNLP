import datetime

from F.DATE import TODAY
from FNLP.LanguageEngines import BaseModel


class BaseVariables:
    _createdDate: datetime = None
    _updatedDate: datetime = TODAY
    _dates_analyzed_count: int = 0
    _dates_analyzed: list = []
    _webpages_analyzed_count: int = 0
    _webpages_analyzed: list = []
    _category_scores = None

class WordVariables:
    word: str = None
    first_letter: str = None
    letter_count: int = None
    isFirstCapital: bool = False

class WordsVariables(BaseModel):
    # Date
    overall_words_by_date = {}
    stop_words_by_date = {}
    # Overall
    overall_counts: dict = {}
    overall_words_counted: int = 0
    # Unique
    unique_words: list = []
    unique_words_counted: int = 0
    # No Stop Words
    overall_stop_counts: dict = {}

class ContentVariables:
    # Main
    input_contents: list = []
    input_contents_by_date: dict = {}
    input_main_content_only: str = ""
    input_main_content_models: list = []
    # Models
    model_words = None
    model_sentences = None
    model_paragraphs = None

class ParagraphsVariables:
    overall_paragraphs: list = []
    overall_paragraphs_counted: int = 0
    paragraphs_by_date: dict = {}

class SentencesVariables:
    overall_sentences: list = []
    overall_sentences_counted: int = 0
    sentences_by_date: dict = {}
