import re
from F import LIST
from F import DATE
from . import Re

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
        locate_month_variant = Re.locate_term_in_str(month_variant, content)
        if locate_month_variant:
            start = locate_month_variant.start()
            end = start + 15
            temp = content[start:end]
            # -> Check for Year immediately after Month
            find_year = Re.str_contains_year(temp)
            year = LIST.get(0, find_year)
            locate_year = Re.locate_term_in_str(year, temp)
            if locate_year:
                year_end = locate_year.end()
                temp2 = content[start:start+year_end]
                # -> Clean Result.
                filter = Re.__remove_special_characters(temp2)
                result = filter.replace("  ", " ").strip()
                return result
    return False