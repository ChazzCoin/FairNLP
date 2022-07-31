import random
import re

import FOS
import FairResources
from FList import LIST
import FMath
from FLog.LOGGER import Log

Log = Log("FAIR.Language")
# from nltk import WordNetLemmatizer
#
# lemmatizer = WordNetLemmatizer()


QUOTES_ENCODINGS = [b'\xe2\x80\x9e', b'\xe2\x80\x9f', b'\xe2\x80\x9d', b'\xe2\x80\x9c']

"""
    -> Tokenizing/Splitting Words from a String.
"""

def is_capital(content: str):
    firstChar = LIST.get(0, content, default=False)
    if firstChar and str(firstChar).isupper():
        return True
    return False

def are_capital(*content: str):
    for item in content:
        if not is_capital(item):
            return False
    return True

def is_period(content:str):
    if str(content) == ".":
        return True
    return False

def are_periods_or_capitals(*content:str):
    for item in content:
        if is_capital(item) or is_period(item):
            return True
    return False

def is_empty(content: str):
    if not content or content == ' ' or content == '' or str(content) == " ":
        return True
    return False

def are_empty(*content: str):
    for item in content:
        if not item or item == ' ' or item == '' or str(item) == " ":
            return True
    return False

def is_quotation(content:str):
    encoded_character = str(content).encode('utf-8')
    if content == '"':
        return True
    elif encoded_character in QUOTES_ENCODINGS:
        return True
    return False

def is_space(content:str):
    if str(content) == ' ':
        return True
    return False

"""
"Hey there B.J. Jones!"
"Hey there bj jones!"
"""
# This one is actually an extremely difficult issue to solve.
def to_sentences(content: str, combineQuotes=True):
    """ALMOST WORKING!!!"""
    ENDERS = ['.', '?', '!']
    content = content.strip().replace("\n", " ").replace("  ", " ")
    current_index = 0
    start_index = 0
    quotation_count = 0
    sentences = []
    for currentChar in content:
        if current_index == len(content) - 1:
            sent = content[start_index:current_index] + currentChar
            sentences.append(sent)
            break
        fullTest = content[start_index:current_index+1]
        print(fullTest)
        plusOneChar = content[current_index + 1]

        if is_quotation(currentChar):
            quotation_count += 1

        if currentChar in ENDERS:
            if is_space(plusOneChar):
                minusOneChar = str(content[current_index - 1])
                minusTwoChar = str(content[current_index - 2])
                minuxThreeChar = str(content[current_index - 3])
                plusTwoChar = str(content[current_index + 2])
                if is_capital(plusTwoChar) or is_quotation(plusTwoChar) and not are_periods_or_capitals(minusOneChar, minusTwoChar, minuxThreeChar):
                    if are_empty(minusOneChar, minusTwoChar, minuxThreeChar):
                        current_index += 1
                        continue
                    if combineQuotes and not FMath.is_even_number(quotation_count):
                        current_index += 1
                        continue
                    sent = content[start_index:current_index] + currentChar
                    start_index = current_index + 2
                    sentences.append(sent)
            elif is_quotation(plusOneChar):
                current_index = current_index + 1
                minusOneChar = str(content[current_index - 2])
                minusTwoChar = str(content[current_index - 3])
                minuxThreeChar = str(content[current_index - 4])
                plusTwoChar = str(content[current_index + 2])
                if is_capital(plusTwoChar) or is_quotation(plusTwoChar) and not are_periods_or_capitals(minusOneChar, minusTwoChar, minuxThreeChar):
                    if are_empty(minusOneChar, minusTwoChar, minuxThreeChar):
                        current_index += 1
                        continue
                    if combineQuotes and not FMath.is_even_number(quotation_count):
                        current_index += 1
                        continue
                    sent = content[start_index:current_index] + '"'
                    start_index = current_index + 2
                    sentences.append(sent)
        current_index += 1
    return sentences

if __name__ == '__main__':
    contentList = FairResources.get_source("test_content")
    content = LIST.get(0, contentList, default="")
    print(content)
    se = to_sentences(content)
    print(se)

def to_paragraphs(body: str) -> [str]:
    """ -> Separates text based on "\n" <- """
    paragraph_list = []
    i = 0
    temp_body = body
    for char in body:
        if char == "\n":
            new_body = temp_body[:i]
            paragraph_list.append(new_body)
            temp_body = temp_body[i+1:]
            i = 0
            continue
        i += 1
    return paragraph_list

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

HAPPY = {
    ":-)",
    ":)",
    ";)",
    ":o)",
    ":]",
    ":3",
    ":c)",
    ":>",
    "=]",
    "8)",
    "=)",
    ":}",
    ":^)",
    ":-D",
    ":D",
    "8-D",
    "8D",
    "x-D",
    "xD",
    "X-D",
    "XD",
    "=-D",
    "=D",
    "=-3",
    "=3",
    ":-))",
    ":'-)",
    ":')",
    ":*",
    ":^*",
    ">:P",
    ":-P",
    ":P",
    "X-P",
    "x-p",
    "xp",
    "XP",
    ":-p",
    ":p",
    "=p",
    ":-b",
    ":b",
    ">:)",
    ">;)",
    ">:-)",
    "<3",
}

SAD = {
    ":L",
    ":-/",
    ">:/",
    ":S",
    ">:[",
    ":@",
    ":-(",
    ":[",
    ":-||",
    "=L",
    ":<",
    ":-[",
    ":-<",
    "=\\",
    "=/",
    ">:(",
    ":(",
    ">.<",
    ":'-(",
    ":'(",
    ":\\",
    ":-c",
    ":c",
    ":{",
    ">:\\",
    ";(",
}