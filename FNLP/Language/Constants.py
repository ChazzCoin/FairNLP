from F import DICT

# from FA.Categories import Topics
from FairResources import FairResources

# WEIGHTED_TERMS = Topics.ALL_CATEGORIES().get_all_weighted_terms()

STOP_WORDS = FairResources.get_stopwords()

SENTENCE_ENDERS = ['.', '?', '!']
QUOTES_ENCODINGS = [b'\xe2\x80\x9e', b'\xe2\x80\x9f', b'\xe2\x80\x9d', b'\xe2\x80\x9c']

ALPHABET_DICT_PAIRS = {"a": "A", "b": "B", "c": "C", "d": "D", "e": "E", "f": "F", "g": "G", "h": "H",
                       "i": "I", "j": "J", "k": "K", "l": "L", "m": "M", "n": "N", "o": "O", "p": "P",
                       "q": "Q", "r": "R", "s": "S", "t": "T", "u": "U", "v": "V", "w": "W", "x": "X",
                       "y": "Y", "z": "Z" }

GET_CAPITAL_FROM_LOWER = lambda lowerChar: DICT.get(lowerChar, ALPHABET_DICT_PAIRS, default=False)
GET_LOWER_FROM_CAPITAL = lambda capitalChar: DICT.get_key(capitalChar, ALPHABET_DICT_PAIRS, default=False)
GET_OPPOSITE_LOWER_OR_UPPER = lambda char: GET_CAPITAL_FROM_LOWER(char) if str(char).islower() else GET_LOWER_FROM_CAPITAL(char)

ALPHABET_LOWER = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
                  "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
ALPHABET_UPPER = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                  "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
ALPHABET_ALL = ALPHABET_LOWER + ALPHABET_UPPER
NUMBERS_SINGLE = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

SUMMARY = lambda first, middle, last: f"{first} {middle} {last}"