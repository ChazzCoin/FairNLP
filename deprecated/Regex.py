import re
from F import LIST
from F import DATE
import FairResources

STOPWORDS = FairResources.get_stopwords()

"""
it claims, sentences.. -> r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s"
"""

def remove_special_characters(text):
    """ DEPRECATED """
    newText = re.sub('[^a-zA-Z0-9]', ' ', text)
    return newText

def search(search_term, content):
    match = re.findall(fr'.*{search_term}.*', content)
    return match if len(match) >= 1 and match is not None else False

def contains(search_term, content):
    try:
        if type(content) in [list, tuple]:
            for itemContent in content:
                match = re.findall(fr'.*{str(search_term)}.*', itemContent)
                if len(match) >= 1 and match is not None:
                    return True
            return False
        else:
            match = re.findall(fr'.*{str(search_term)}.*', content)
            return True if len(match) >= 1 and match is not None else False
    except Exception as e:
        print(f"Failed to regex findall. {str(search_term)}, error=[ {e} ]")
        return False

def contains_strict(search_term, content):
    try:
        if type(content) in [list, tuple]:
            for itemContent in content:
                search_term = remove_special_characters(search_term)
                match = re.findall(fr'\b{search_term}\b', itemContent)
                if len(match) >= 1 and match is not None:
                    return True
            return False
        else:
            search_term = remove_special_characters(search_term)
            match = re.findall(fr'\b{search_term}\b', content)
            return True if len(match) >= 1 and match is not None else False
    except Exception as e:
        print(f"Failed to regex findall. {search_term}, error=[ {e} ]")
        return False

def contains_any(search_terms, content):
    search_terms = LIST.flatten(search_terms)
    for term in search_terms:
        temp = contains(term, content)
        if temp:
            return True
    return False

def str_contains_year(content):
    match = re.findall(r'\b[1-2][0-9][0-9][0-9]\b', content)
    if match and len(match) >= 1:
        if LIST.get(0, match) == "":
            return False

        newMatch = []
        for year in match:
            if len(year) > 4:
                continue
            if int(year) > int(DATE.get_current_year()):
                continue
            if int(year) < 1900:
                continue

            newMatch.append(year)
        return newMatch

def locate_term_in_str(term, content):
    match = re.search(fr'\b{term}\b', content)
    if match:
        return match
    return False

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
        if str(char).isupper() and previous_char == " " and not start_enabled:
            start_index = current_index
            start_enabled = True
        if str(char).islower() and previous_char == " " and start_enabled:
            end_index = current_index
            words = content[start_index:end_index-1]
            temp_words.append(words)
            start_enabled = False
        previous_char = char
        current_index += 1
    final_words = []
    for word in temp_words:
        if word.lower() in STOPWORDS:
            continue
        final_words.append(word)
    return final_words

# if __name__ == '__main__':
#     testing3 = "Most of these picks seemed to be right in Buffett's wheelhouse. He has become a big fan of energy stocks lately. The large new stake in Occidental Petroleum isn't surprising. Buffett likes the financial services industry. Ally Financial and Citigroup certainly represent the kinds of financial stocks that he's favored in the past."
#     testing = "Abercrombie & Fitch lost more than 30% in premarket trading, set to become the latest retail stock disaster. The specialty retailer on Tuesday reported an unexpected quarterly loss, despite better-than-expected revenue. Analysts had expected a profit. Freight and product costs weighed on results. Abercrombie also cut its sales outlook for fiscal 2022, anticipating that the current economic headwinds will remain at least through the end of the year."
#     testing2 = "Snap shares plunged more than 30% in Tuesday’s premarket, the morning after the social media company issued a warning about its upcoming second-quarter results and said it would slow hiring. The Snapchat parent said it’s dealing with a number of issues, including inflation, an uncertain economic environment and Apple’s privacy policy changes."
#     test = extract_only_capital_words_manual(testing3)
#     print(test)
"""
1. March 02 2022
2. 03/02/2022
3. 03-02-2022
4. 2022-03-02
"""
def extract_date(content):
    """ EXPERIMENTAL AND NOT FINISHED! """
    if type(content) not in [str]:
        content = str(content)
    all = []
    months = DATE.months.keys()
    for item in months:
        all.append(item)
    month_variants = DATE.months.values()
    for item in month_variants:
        all.append(item)
    temp_all = LIST.flatten(all)
    _all = LIST.remove_duplicates(temp_all)
    for month_variant in _all:
        # -> Check for any Month or Month Variant in Full String
        locate_month_variant = locate_term_in_str(month_variant, content)
        if locate_month_variant:
            start = locate_month_variant.start()
            end = start + 15
            temp = content[start:end]
            # -> Check for Year immediately after Month
            find_year = str_contains_year(temp)
            year = LIST.get(0, find_year)
            locate_year = locate_term_in_str(year, temp)
            if locate_year:
                year_end = locate_year.end()
                temp2 = content[start:start+year_end]
                # -> Clean Result.
                filter = remove_special_characters(temp2)
                result = filter.replace("  ", " ").strip()
                return result
    return False