from F import LIST, DICT
from F.LOG import Log
from FNLP.Engines.Words.Frequency import get_frequency_count_of_words
from FNLP.Language import Words, Constants


def analyze_content(tokens, top_words_count=500):
    word_count = len(tokens)
    # -> Filter Out The Crap + Stop Words
    # -> Add Dictionary Check to see if its a word.
    unique_words = []
    no_stop_words = []
    for word in Log.ProgressBarYielder(tokens, prefix="Analyzing Content"):
        if not Words.is_potentially_a_word(word):
            continue
        word = str(word).lower()
        unique_words.append(word)
        if word in Constants.STOP_WORDS:
            continue
        no_stop_words.append(word)
    # -> Finish Up
    unique_words = LIST.remove_duplicates(unique_words)
    scores = get_frequency_count_of_words(tokens)
    stop_scores = get_frequency_count_of_words(no_stop_words)
    stop_scores = DICT.order_by_value(stop_scores)
    top_x_words = _top_x(stop_scores, top_words_count)
    return { "words_counted": word_count, "unique_words": unique_words, "scores": scores, "stop_scores": stop_scores, "top_x_words": top_x_words }

def _top_x(objs:dict, x:int=20):
    top_objs = []
    i = 0
    for key in objs:
        if i >= x:
            break
        top_objs.append((key, objs[key]))
        i += 1
    return top_objs

"""
    --> Analyzers! <--
"""

def analyze_word(word:str):
    """ GET: FirstLetter (lower), isFirstLetterCapital, LetterCount """
    try:
        firstLetter = str(word[0]).lower()
        firstLetterCapital = Words.is_capital(word)
        letterCount = len(word)
        return { "first_letter": firstLetter, "isFirstCapital": firstLetterCapital, "letter_count": letterCount }
    except Exception as e:
        print(f"Failed to Analyze Word: [ {word} ]")
        return None

def get_all_words_scores(words:[]) -> {}:
    """ Count how many times a word is seen. """
    return get_frequency_count_of_words(words)

def get_overall_word_count(words:[]) -> int:
    """ Count how many words have been seen overall. """
    return len(words)

def get_all_unique_words(tokens:[str]) -> [str]:
    """ Remove any duplicate words. """
    unique_words = []
    for word in tokens:
        if not Words.is_potentially_a_word(word):
            continue
        word = str(word).lower()
        unique_words.append(word)
    return unique_words