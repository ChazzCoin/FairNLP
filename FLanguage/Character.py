from . import Constants
from FList import LIST

def is_in_alphabet_lower(content:str):
    firstChar = LIST.get(0, content, default=False)
    if firstChar in Constants.ALPHABET_LOWER:
        return True
    return False

def is_in_alphabet_upper(content:str):
    firstChar = LIST.get(0, content, default=False)
    if firstChar in Constants.ALPHABET_UPPER:
        return True
    return False

def is_in_alphabet(content:str):
    firstChar = LIST.get(0, content, default=False)
    if firstChar in Constants.ALPHABET_ALL:
        return True
    return False

def is_single_number(content):
    if type(content) != int:
        content = LIST.get(0, content, default=False)
    if content in Constants.NUMBERS_SINGLE:
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
    elif encoded_character in Constants.QUOTES_ENCODINGS:
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
    if str(content) in Constants.SENTENCE_ENDERS:
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