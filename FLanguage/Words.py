from FList import LIST
from FLanguage import Utils, Character, Constants
from fairNLP import Regex

def find_proper_nouns(content:str):
    return Regex.extract_only_capital_words_regex(content)

def make_capital(word:str):
    firstChar = word[0]
    newWord = word[1:]
    if Character.is_in_alphabet(firstChar) and not Character.is_capital(firstChar):
        firstChar = Constants.GET_CAPITAL_FROM_LOWER(firstChar)
    newWord = firstChar + newWord
    return newWord

def make_lower(word:str):
    firstChar = word[0]
    newWord = word[1:]
    if Character.is_in_alphabet(firstChar) and Character.is_capital(firstChar):
        firstChar = Constants.GET_LOWER_FROM_CAPITAL(firstChar)
    newWord = firstChar + newWord
    return newWord

def to_x_grams(tokens, x):
    """ PUBLIC """
    if type(tokens) == str:
        tokens = to_words_v1(tokens)
    i = 0
    x_grams = []
    if len(tokens) < x:
        print("found none", tokens)
        return x_grams
    for _ in tokens:
        if i+x > len(tokens):
            break
        phrase = ""
        for c in range(x):
            phrase = combine_words(phrase, tokens[i+c])
        x_grams.append(phrase)
        i += 1
    return x_grams

def to_words_v1(content: str):
    content = Utils.replace(content, ".", ",", ";", "\n", "  ")
    s = content.split(" ")
    newS = Utils.remove_empty_strings(s)
    return newS

def to_bi_grams_v2(tokens):
    """ PUBLIC HELPER """
    return to_x_grams(tokens, 2)

def to_tri_grams_v2(tokens):
    """ PUBLIC HELPER """
    return to_x_grams(tokens, 3)

def to_quad_grams_v2(tokens):
    """ PUBLIC HELPER """
    return to_x_grams(tokens, 4)

def expand_word(word: str) -> []:
    """ PUBLIC -> FAIR Expansion <- """
    word_lower = word.lower()
    word_upper = word.upper()
    word_first_capital = word[0].upper() + word[1:]
    # word_stem = lemmatize_word(word)
    # word_stem_first_capital = word_stem[0].upper() + word_stem[1:]
    return [word, word_lower, word_upper, word_first_capital]

def score_words(words):
    result = {}
    for word in words:
        if word in result.keys():
            tempValue = result[word]
            result[word] = tempValue + 1
        else:
            result[word] = 1
    return result

def combine_words(*words):
    """ Combines two strings together. """
    temp_word = ""
    words = LIST.flatten(words)
    if len(words) > 0:
        for word in words:
            temp_word += " " + word.strip()
        return temp_word.strip()
    return str(words).strip()

def remove_ing(word):
    if word.endswith("ing"):
        return word[:-3]
    elif word.endswith("ings"):
        return word[:-4]
    return False

def remove_apos(word):
    word = word.replace("'", "")
    return word

def __split_words(text):
    """ ALTERNATIVE: Split a string into array of words. """
    try:
        import re
        text = re.sub(r'[^\w ]', '', text)  # strip special chars
        return [x.strip('.').lower() for x in text.split()]
    except TypeError:
        return None