

"""
-> if CurrentCharacter is '.'
    - > if three previous characters are not periods
    - > if first next character is a space
    - > if second next character is a sentence beginner
"""
# This one is actually an extremely difficult issue to solve.
from FNLP.Language import Character
from F import MATH
from FNLP.Language import Constants

FORM_SENTENCE = lambda strContent, startIndex, endIndex, caboose: f"{strContent[startIndex:endIndex]}{caboose}"

def to_sentences(content: str, combineQuotes=True):
    """100%! WORKING!!!"""
    content = __prepare_content_for_sentence_extraction(content)
    current_index, start_index, quotation_count, sentences = 0, 0, 0, []
    # -> Loop every character in content (str).
    for currentChar in content:
        # -> Verify we have next (+3) characters.
        if current_index >= len(content) - 3:
            if MATH.is_even_number(quotation_count + 1):
                sent = content[start_index:-1] + currentChar + '"'
            else:
                sent = content[start_index:-1] + currentChar
            sentences.append(sent)
            break
        plusOneChar = content[current_index + 1]
        # -> Keep count of quotations. Even = Closed and Odd = Open
        if Character.is_quotation(currentChar):
            quotation_count += 1
        # -> Verify current (0) character is a "sentence ending character" EX: . ! ?
        if __is_sentence_ender(currentChar):
            # -> Verify next (+1) character is a space or quote "
            if Character.is_space(plusOneChar) or Character.is_quotation(plusOneChar):
                QM = False
                # -> Verify next (+1) character is a quotation and are we "Quote Closed"
                if Character.is_quotation(plusOneChar) and MATH.is_even_number(quotation_count + 1):
                    QM = True
                plusTwoChar = str(content[current_index + 2])
                plusThreeChar = str(content[current_index + 3])
                # -> Verify that +2 character is a valid "Sentence Beginner"
                if __is_sentence_beginner(plusTwoChar if not QM else plusThreeChar):
                    # -> Verify next character is a space
                    if Character.is_space(plusOneChar if not QM else plusTwoChar):
                        minusOneChar = str(content[current_index - 1])
                        minusTwoChar = str(content[current_index - 2])
                        minuxThreeChar = str(content[current_index - 3])
                        # -> Verify previous three characters do not include a period
                        if not Character.are_periods(minusOneChar, minusTwoChar, minuxThreeChar):
                            if combineQuotes and not MATH.is_even_number(quotation_count if not QM else quotation_count + 1):
                                current_index += 1
                                continue
                            # -> VERIFIED! Create sentence.
                            sent = FORM_SENTENCE(content, start_index, current_index, currentChar if not QM else f'{currentChar}"')
                            start_index = current_index + 2
                            sentences.append(sent)
        current_index += 1
    return sentences


def __prepare_content_for_sentence_extraction(content):
    return content.strip().replace("\n", " ").replace("  ", " ")

def __is_sentence_ender(content):
    if str(content) in Constants.SENTENCE_ENDERS:
        return True
    return False

def __is_sentence_beginner(content):
    if Character.is_in_alphabet(content):
        return True
    elif Character.is_quotation(content):
        return True
    elif Character.is_single_number(content):
        return True
    return False