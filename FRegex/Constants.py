SEARCH_TERM = lambda searchTerm: fr'.*{str(searchTerm)}.*'
SEARCH_TERM_TWO = lambda searchTerm: fr'\b{searchTerm}\b'
REMOVE_SPECIAL_CHARACTERS = r'[^a-zA-Z0-9]'

CONTAINS_YEAR = r'\b[1-2][0-9][0-9][0-9]\b'
ONLY_CAPITAL_WORDS = r'([A-Z][a-z]+)'

EXTRACT_TICKERS_STRICT = r'[^\s$:(][A-Z]{1,5}(?=\s|\)|/|,|\.)'
EXTRACT_TICKERS_LIGHT = r'[^\s$:(][A-Za-z]{1,5}(?=\s|\)|/|,|\.)'

IS_URL = r'http.?://.*/'
FIND_URLS = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
