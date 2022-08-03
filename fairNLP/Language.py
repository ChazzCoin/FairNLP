import FairResources
# from Categories import Topics

from FList import LIST
import FMath
from FLog.LOGGER import Log

Log = Log("FAIR.Language.DEPRECATED")

"""
    ->  DEPRECATED!!!!!  <-
"""

# WEIGHTED_TERMS = Topics.ALL_CATEGORIES().get_all_weighted_terms()

STOP_WORDS = FairResources.get_stopwords()

SENTENCE_ENDERS = ['.', '?', '!']
QUOTES_ENCODINGS = [b'\xe2\x80\x9e', b'\xe2\x80\x9f', b'\xe2\x80\x9d', b'\xe2\x80\x9c']

ALPHABET_LOWER = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
                  "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
ALPHABET_UPPER = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                  "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
ALPHABET_ALL = ALPHABET_LOWER + ALPHABET_UPPER
NUMBERS_SINGLE = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

SUMMARY = lambda first, middle, last: f"{first} {middle} {last}"
"""
    ->  DEPRECATED!!!!!  <-
"""

def is_in_alphabet_lower(content:str):
    firstChar = LIST.get(0, content, default=False)
    if firstChar in ALPHABET_LOWER:
        return True
    return False

def is_in_alphabet_upper(content:str):
    firstChar = LIST.get(0, content, default=False)
    if firstChar in ALPHABET_UPPER:
        return True
    return False

def is_in_alphabet(content:str):
    firstChar = LIST.get(0, content, default=False)
    if firstChar in ALPHABET_ALL:
        return True
    return False

def is_single_number(content):
    if type(content) != int:
        content = LIST.get(0, content, default=False)
    if content in NUMBERS_SINGLE:
        return True
    return False

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

def are_periods(*content: str):
    for item in content:
        if not is_period(item):
            return False
    return True

def is_period(content:str):
    firstChar = LIST.get(0, content, default=False)
    if firstChar and str(content) == ".":
        return True
    return False

def are_periods_or_capitals(*content:str):
    for item in content:
        if is_capital(item) or is_period(item):
            return True
    return False

def is_empty(content: str):
    firstChar = LIST.get(0, content, default=False)
    if firstChar and not content or content == ' ' or content == '' or str(content) == " ":
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
    firstChar = LIST.get(0, content, default=False)
    if firstChar and str(content) == ' ':
        return True
    return False

def is_space_or_quotation(content):
    if is_quotation(content) or is_space(content):
        return True
    return False

def __is_sentence_ender(content):
    if str(content) in SENTENCE_ENDERS:
        return True
    return False

def __is_sentence_beginner(content):
    if is_in_alphabet(content):
        return True
    elif is_quotation(content):
        return True
    elif is_single_number(content):
        return True
    return False

def __prepare_content_for_sentence_extraction(content):
    return content.strip().replace("\n", " ").replace("  ", " ")


def __compare(one, two):
    listone, listtwo = [], []
    for item1 in one:
        if item1 in two:
            continue
        listone.append(item1)

    for item2 in two:
        if item2 in one:
            continue
        listtwo.append(item2)

    return listone, listtwo

"""
-> if CurrentCharacter is '.'
    - > if three previous characters are not periods
    - > if first next character is a space
    - > if second next character is a sentence beginner
"""
# This one is actually an extremely difficult issue to solve.
def to_sentences(content: str, combineQuotes=True):
    """100%! WORKING!!!"""
    content = __prepare_content_for_sentence_extraction(content)
    current_index, start_index, quotation_count, sentences = 0, 0, 0, []
    for currentChar in content:
        if current_index >= len(content) - 3:
            if FMath.is_even_number(quotation_count + 1):
                sent = content[start_index:-1] + currentChar + '"'
            else:
                sent = content[start_index:-1] + currentChar
            sentences.append(sent)
            break
        plusOneChar = content[current_index + 1]
        if is_quotation(currentChar):
            quotation_count += 1
        if __is_sentence_ender(currentChar):
            if is_space(plusOneChar) or is_quotation(plusOneChar):
                QM = False
                if is_quotation(plusOneChar) and FMath.is_even_number(quotation_count+1):
                    QM = True
                minusOneChar = str(content[current_index - 1])
                minusTwoChar = str(content[current_index - 2])
                minuxThreeChar = str(content[current_index - 3])
                plusTwoChar = str(content[current_index + 2])
                plusThreeChar = str(content[current_index + 3])
                # i + 1 -> Check if beginning of next sentencer is valid
                if __is_sentence_beginner(plusTwoChar if not QM else plusThreeChar):
                    # i + 2 -> Check if
                    if is_space(plusOneChar if not QM else plusTwoChar):
                        if not are_periods(minusOneChar, minusTwoChar, minuxThreeChar):
                            if combineQuotes and not FMath.is_even_number(quotation_count if not QM else quotation_count + 1):
                                current_index += 1
                                continue
                            sent = content[start_index:current_index] + currentChar if not QM else content[start_index:current_index] + f'{currentChar}"'
                            start_index = current_index + 2
                            sentences.append(sent)
        current_index += 1
    return sentences

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

# # -> master summarizer!
# def summarize(content='', max_sents=5):
#     if not content or max_sents <= 0:
#         return []
#     keepList = []
#     # Pre. -> Convert raw string of text into a List of Sentences.
#     sentences = to_sentences(content)
#     if not sentences:
#         return False
#     # 1. -> If only 6 or less sentences to start, return now
#     if len(sentences) <= 6:
#         return combine_words(sentences)
#     # 2. -> Always use the first and last sentence
#     firstSentence = LIST.get(0, sentences, False)
#     if not firstSentence:
#         return False
#     lastIndex = len(keepList) - 1
#     lastSentence = LIST.get(lastIndex, sentences, False)
#     if len(lastSentence) <= 50:
#         lastSentence = LIST.get(lastIndex - 1, sentences, False)
#     # 3. -> Remove First and Last Sentence
#     without_first = LIST.remove_index(0, sentences)
#     without_first_and_last = without_first[:-1]
#     # 4. -> Filter out by length
#     for sen in without_first_and_last:
#         l = len(sen)
#         if 50 < l > 400:
#             continue
#         keepList.append(sen)
#     # 5. -> Section off list into three parts.
#     #           - Beginning, Middle, End.
#     base_count = int(len(keepList) / 3)
#     middle_count = base_count * 2
#     first = keepList[:base_count]
#     middle = keepList[base_count:middle_count]
#     last = keepList[middle_count:]
#     # 6. -> Score each Section
#     first_scored = Topics.ALL_CATEGORIES().score_categorizer(first)
#     middle_scored = Topics.ALL_CATEGORIES().score_categorizer(middle)
#     last_scored = Topics.ALL_CATEGORIES().score_categorizer(last)
#     # 7. -> Filter/Select highest scored sentences from each Section.
#     first_summary = form_summary(first_scored, 1)
#     middle_summary = form_summary(middle_scored, 1)
#     last_summary = form_summary(last_scored, 1)
#     # 8. -> Combine all 3 Sections into 1 Single Body of Text.
#     combined_summary = combine_words(first_summary, middle_summary, last_summary)
#     # 9. -> Combine the first sentence, the middle body and the last sentence to form "The_Summary"
#     The_Summary = SUMMARY(firstSentence, combined_summary, lastSentence)
#     return The_Summary

def form_summary(scored_sentences: [], max_sent=5):
    final_list = []
    total_count = len(scored_sentences) - 1
    current_index = 0
    sorted_scored_sentences = sorted(scored_sentences, key=lambda lst: lst[0], reverse=True)
    while current_index <= total_count:
        if len(final_list) >= max_sent:
            break
        raw_sent = LIST.get(current_index, sorted_scored_sentences)
        sent = LIST.get(1, raw_sent)
        # - Finish up
        final_list.append(sent)
        current_index += 1
    the_summary = combine_words(final_list)
    return the_summary

def __split_words(text):
    """ ALTERNATIVE: Split a string into array of words. """
    try:
        import re
        text = re.sub(r'[^\w ]', '', text)  # strip special chars
        return [x.strip('.').lower() for x in text.split()]
    except TypeError:
        return None

def keywords(content):
    """Get the top 10 keywords and their frequency scores ignores blacklisted
    words in stopwords, counts the number of occurrences of each word, and
    sorts them in reverse natural order (so descending) by number of
    occurrences.
    """
    NUM_KEYWORDS = 10
    content = __split_words(content)
    # of words before removing blacklist words
    if content:
        num_words = len(content)
        content = [x for x in content if x not in STOP_WORDS]
        freq = {}
        for word in content:
            if word in freq:
                freq[word] += 1
            else:
                freq[word] = 1

        min_size = min(NUM_KEYWORDS, len(freq))
        keywords = sorted(freq.items(),
                          key=lambda x: (x[1], x[0]),
                          reverse=True)
        keywords = keywords[:min_size]
        keywords = dict((x, y) for x, y in keywords)
        for k in keywords:
            articleScore = keywords[k] * 1.0 / max(num_words, 1)
            keywords[k] = articleScore * 1.5 + 1
        return dict(keywords)
    else:
        return dict()

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