import datetime

from F.DATE import TODAY

class BaseVariables:
    # Internal Only
    _webpage_models = []
    # Main
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

class WordsVariables:
    input_w_content = []
    input_w_tokens = []
    # Analyzer
    words_counted: int = 0
    unique_words: list = []
    unique_words_count: int = 0
    counts: dict = {}
    stop_counts: dict = {}
    top_x_words: dict = {}

class ContentVariables:
    # Main
    input_contents: list = []
    input_tokens: list = []
    input_tokens_by_content: list = []
    input_main_content_only: str = ""
    # Models
    model_words = None
    model_sentences = None
    model_paragraphs = None


class ParagraphVariables:
    input_p_content = None
    paragraphs: list = []
    paragraph_count: int = 0

class SentenceVariables:
    input_s_raw = None
    input_s_content = ""
    sentences: list = []
    sentence_count: int = 0

