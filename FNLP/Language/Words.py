from F import LIST, DICT
from FNLP.Language import Utils, Character, Constants
from FNLP.Regex import ReWords



""" 
- input: Takes in two lists to match
- output: ( Overall_Score, { matched_term: count } 
"""
def matcher(word_list: list, weighted_terms: list, score_variant=0.6) -> (int,{}):
    # 2. -> Loop Each Category Weighted Term
    temp_dict = {}  # { "weighted_term": "match_count" }
    score = 0  # "weighted_term" Score * "match_count"
    for w_term in weighted_terms:
        # Stay Safe People
        if not w_term or w_term == "" or w_term == " ":
            continue
        # -> Expand Weighted Term
        # expanded_key_list = expand_word(w_term)
        # 3. -> Loop All Tokens AND MATCH!!
        for token in word_list:
            # Stay Safe People
            if not token or token == "" or token == " ":
                continue
            # MATCHER! -> if content word is in expanded weighted term list...
            no_the_token = remove_the(token)
            score_phrase = phrase_match_percentage(token, w_term)
            score_no_the = phrase_match_percentage(no_the_token, w_term)
            if score_phrase >= score_variant or score_no_the >= score_variant:
            # if token == w_term or no_the_token == w_term:
                # -> We have a match!
                key_score = 1
                score += key_score
                temp_dict = DICT.add_matched_word_to_result(token, temp_dict)
    # -> 4. Finish Up
    return score, temp_dict  # ( score, { "weighted_term": "match_count", "weighted_term": "match_count" } )

def matcher_with_expander(word_list: list, weighted_terms: list) -> (int,{}):
    # 2. -> Loop Each Category Weighted Term
    temp_dict = {}  # { "weighted_term": "match_count" }
    score = 0  # "weighted_term" Score * "match_count"
    for w_term in weighted_terms:
        # Stay Safe People
        if not w_term or w_term == "" or w_term == " ":
            continue
        # -> Expand Weighted Term
        expanded_key_list = expand_word(w_term)
        # 3. -> Loop All Tokens AND MATCH!!
        for token in word_list:
            # Stay Safe People
            if not token or token == "" or token == " ":
                continue
            # MATCHER! -> if content word is in expanded weighted term list...
            if is_match(token, expanded_key_list):
                # -> We have a match!
                key_score = 1
                score += key_score
                temp_dict = DICT.add_matched_word_to_result(w_term, temp_dict)
    # -> 4. Finish Up
    return score, temp_dict  # ( score, { "weighted_term": "match_count", "weighted_term": "match_count" } )

def phrase_match_percentage(phrase_one, phrase_two):
    pListOne = to_words_v1(phrase_one)
    pListTwo = to_words_v1(phrase_two)
    poneCount = len(pListOne)
    ptwoCount = len(pListTwo)
    if poneCount > ptwoCount:
        highest = poneCount
    else:
        highest = ptwoCount
    result = 0
    for i in range(highest):
        poneword = LIST.get(i, pListOne, False)
        ptwoword = LIST.get(i, pListTwo, False)
        if poneword == ptwoword:
            result += 1
    r = result / highest
    return r

def find_proper_nouns(content:str):
    raw = ReWords.extract_only_capital_words_regex(content)
    proper_nouns = []
    for word in raw:
        if str(word).lower() in Constants.STOP_WORDS:
            continue
        proper_nouns.append(word)
    return proper_nouns

def find_proper_nouns_v2(content:str):
    tokens = to_words_v1(content)
    proper_nouns = []
    temp = []
    for word in tokens:
        if is_capital(word):
            if str(word).lower() in Constants.STOP_WORDS:
                continue
            temp.append(word)
        else:
            if temp:
                proper_nouns.append(temp)
                temp = []
    return proper_nouns

def is_match(word:str, word_list:list, ignoreCapitals=False):
    if ignoreCapitals:
        word = str(word).lower() # Make LowerCase
        word_list = [str(item).lower() for item in word_list] # Make All Lowercase
    if word in word_list:
        return True
    return False

def is_capital(word:str):
    firstChar = word[0]
    if str(firstChar).isupper():
        return True
    return False

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

def remove_the(word:str):
    word = word.strip()
    if word.startswith("the") or word.startswith("The"):
        word = word.replace("the", "").replace("The", "")
        return word.strip()
    return word

def __split_words(text):
    """ ALTERNATIVE: Split a string into array of words. """
    try:
        import re
        text = re.sub(r'[^\w ]', '', text)  # strip special chars
        return [x.strip('.').lower() for x in text.split()]
    except TypeError:
        return None


if __name__ == '__main__':
    wordOne = "Sandbox development"
    wordTwo = "The Sandbox"
    print(phrase_match_percentage(wordOne, wordTwo))