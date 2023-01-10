from F import LIST
from FNLP.Language import Words, Constants, Tokenizer

"""
    -> Engine to analyze words by count of times it has been seen within an article.
    - word, score, content_count, word_count
"""

def analyze_content(content:str):
    # tokenize words
    tokens = Words.to_words_v2(content)
    word_count = len(tokens)
    # -> Filter Out The Crap + Stop Words
    # -> Add Dictionary Check to see if its a word.
    unique_words = []
    no_stop_words = []
    for word in tokens:
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
    return { "word_count": word_count, "unique_words": unique_words, "scores": scores, "stop_scores": stop_scores }

def score_words(words: list) -> dict:
    result = {}
    for word in words:
        if word in result.keys():
            tempValue = result[word]
            result[word] = tempValue + 1
        else:
            result[word] = 1
    return result

# -> Takes word count dicts and add the values into one count.
def add_word_frequency_counts(*dicts) -> dict:
    """ Add two dicts of word counts together """
    result = {}
    # -> Loop each dictionary
    dicts = LIST.flatten(dicts)
    for dictionary in dicts:
        # Loop each key
        for key in dictionary.keys():
            if result.__contains__(key):
                temp = result[key] + dictionary[key]
                result[key] = temp
            else:
                result[key] = dictionary[key]
    return result

def get_frequency_count_of_words(words:list) -> dict:
    """ TIFFANY """
    result = {}
    for item in words:
        result = add_matched_word_to_result(item, result)
    return result

def add_matched_word_to_result(word: str, dic: dict) -> dict:
    """ TIFFANY """
    if word in dic.keys():
        dic[word] += 1
    else:
        dic[word] = 1
    return dic


if __name__ == '__main__':
    test = "i am a guilty stupid little whore of a person named John Adams the very second!"
    results = analyze_content(test)
    print(results)