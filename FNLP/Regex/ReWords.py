import re
from FNLP.Language.Constants import STOP_WORDS
from FNLP.Language import Character


def extract_only_capital_words_regex(content):
    capital_words = re.findall(r'([A-Z][a-z]+)', content)
    return capital_words

def extract_only_capital_words_manual(content):
    previous_char = " "
    current_index = 0
    start_index = 0
    start_enabled = False
    temp_words = []
    for char in content:
        if Character.is_capital(char) and Character.is_empty(char) and not start_enabled:
            start_index = current_index
            start_enabled = True
        if not Character.is_capital(char) and Character.is_empty(char) and start_enabled:
            end_index = current_index
            words = content[start_index:end_index-1]
            temp_words.append(words)
            start_enabled = False
        previous_char = char
        current_index += 1
    final_words = []
    for word in temp_words:
        if word.lower() in STOP_WORDS:
            continue
        final_words.append(word)
    return final_words