import random
import re

from FList import LIST
from FLog.LOGGER import Log

Log = Log("FAIR.Language")
# from nltk import WordNetLemmatizer
#
# lemmatizer = WordNetLemmatizer()

"""
    -> Tokenizing/Splitting Words from a String.
"""

def to_sentences(content: str):
    content = content.replace("\n", "").strip()
    s = content.split(". ")
    newS = remove_empty_strings(s)
    # finalS = []
    # for item in newS:
    #     finalS.append(item + ".")
    newS = re.findall(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", content)
    return newS

def to_words_v1(content: str):
    content = replace(content, ".", ",", ";", "\n", "  ")
    s = content.split(" ")
    newS = remove_empty_strings(s)
    return newS

def remove_empty_strings(list_of_strs: []):
    newS = []
    for word in list_of_strs:
        if word == '':
            continue
        newS.append(word)
    return newS

def replace(content, *args):
    for arg in args:
        content = content.replace(arg, " ")
    return content

def score_complete_tokenization(tokenization: dict):
    result = {}
    for key in tokenization.keys():
        token_list = tokenization[key]
        result[key] = score_words(token_list)
    return result

# @Ext.safe_args
def complete_tokenization_v2(*content, toList=True):
    """ PUBLIC """
    content = LIST.flatten(content)
    toStr = LIST.to_str(content)
    tokens = to_words_v1(toStr)
    bi_grams = to_x_grams(tokens, 2)
    tri_grams = to_x_grams(tokens, 3)
    quad_grams = to_x_grams(tokens, 4)
    if toList:
        return tokens + bi_grams + tri_grams + quad_grams
    else:
        return {"tokens": tokens, "bi_grams": bi_grams, "tri_grams": tri_grams, "quad_grams": quad_grams}

def to_x_grams(tokens, x):
    """ PUBLIC """
    if type(tokens) == str:
        tokens = to_words_v1(tokens)
    i = 0
    x_grams = []
    if len(tokens) < x:
        Log.d("found none", tokens)
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

def to_bi_grams_v2(tokens):
    """ PUBLIC HELPER """
    return to_x_grams(tokens, 2)

def to_tri_grams_v2(tokens):
    """ PUBLIC HELPER """
    return to_x_grams(tokens, 3)

def to_quad_grams_v2(tokens):
    """ PUBLIC HELPER """
    return to_x_grams(tokens, 4)

"""
    -> WORD EXPANSION 
"""
def expand_word(word: str) -> []:
    """ PUBLIC -> FAIR Expansion <- """
    word_lower = word.lower()
    word_upper = word.upper()
    word_first_capital = word[0].upper() + word[1:]
    # word_stem = lemmatize_word(word)
    # word_stem_first_capital = word_stem[0].upper() + word_stem[1:]
    return [word, word_lower, word_upper, word_first_capital]

# def lemmatize_word(word):
#     """ PUBLIC """
#     temp = remove_ing(word)
#     if temp:
#         return temp
#     return lemmatizer.lemmatize(word)

def tokenize_content_into_sentences(content):
    """ Split a large string into sentences """
    sentences = to_sentences(content)
    sentences = [x.replace('\n', '') for x in sentences if len(x) > 10]
    return sentences

def text_summarizer(content='', max_sents=5):
    from fopTopic.Topic import Topic
    if not content or max_sents <= 0:
        return []
    keepList = []
    sentences = tokenize_content_into_sentences(content)
    for sen in sentences:
        l = len(sen)
        if 50 < l > 300:
            continue
        keepList.append(sen)

    firstSentence = keepList[0]
    new_keep = LIST.remove_index(0, keepList)
    temp = Topic.ALL_CATEGORIES().score_categorizer(new_keep)
    final_summary = firstSentence + " " + form_summary(temp, max_sents)
    return final_summary

if __name__ == '__main__':
    text_summarizer("aoidjodfijoifajisdof", 5)

def form_summary(scored_sentences: [], max_sent=5):
    final_list = []
    total_count = len(scored_sentences) - 1
    current_count = 0
    while current_count <= total_count:
        if len(final_list) >= max_sent + 1:
            break
        random_sentence = random.choice(scored_sentences)
        scored_sentences.remove(random_sentence)
        sent = LIST.get(1, random_sentence)
        final_list.append(sent)
        current_count += 1
    the_summary = combine_words(final_list)
    return the_summary


"""
    -> FAIR UTILS
"""

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

# @Ext.safe_args
def combine_args_str(*content: str) -> str:
    temp = ""
    content = LIST.flatten(content)
    for item in content:
        temp += " " + str(item)
        Log.d(temp)
    return str(temp).strip()

def remove_ing(word):
    if word.endswith("ing"):
        return word[:-3]
    elif word.endswith("ings"):
        return word[:-4]
    return False

def remove_apos(word):
    word = word.replace("'", "")
    return word
