from FA.Categories import Topics
from F import LIST
from . import Sentences
from . import Words
from FNLP.Language import Constants

# -> master summarizer!
def summarize(content='', max_sents=5):
    if not content or max_sents <= 0:
        return []
    keepList = []
    # Pre. -> Convert raw string of text into a List of Sentences.
    sentences = Sentences.to_sentences(content)
    if not sentences:
        return False
    # 1. -> If only 6 or less sentences to start, return now
    if len(sentences) <= 6:
        return Words.combine_words(sentences)
    # 2. -> Always use the first and last sentence
    firstSentence = LIST.get(0, sentences, False)
    if not firstSentence:
        return False
    lastIndex = len(keepList) - 1
    lastSentence = LIST.get(lastIndex, sentences, False)
    if len(lastSentence) <= 50:
        lastSentence = LIST.get(lastIndex - 1, sentences, False)
    # 3. -> Remove First and Last Sentence
    without_first = LIST.remove_index(0, sentences)
    without_first_and_last = without_first[:-1]
    # 4. -> Filter out by length
    for sen in without_first_and_last:
        l = len(sen)
        if 50 < l > 400:
            continue
        keepList.append(sen)
    # 5. -> Section off list into three parts.
    #           - Beginning, Middle, End.
    base_count = int(len(keepList) / 3)
    middle_count = base_count * 2
    first = keepList[:base_count]
    middle = keepList[base_count:middle_count]
    last = keepList[middle_count:]
    # 6. -> Score each Section
    first_scored = Topics.ALL_CATEGORIES().score_categorizer(first)
    middle_scored = Topics.ALL_CATEGORIES().score_categorizer(middle)
    last_scored = Topics.ALL_CATEGORIES().score_categorizer(last)
    # 7. -> Filter/Select highest scored sentences from each Section.
    first_summary = form_summary(first_scored, 1)
    middle_summary = form_summary(middle_scored, 1)
    last_summary = form_summary(last_scored, 1)
    # 8. -> Combine all 3 Sections into 1 Single Body of Text.
    combined_summary = Words.combine_words(first_summary, middle_summary, last_summary)
    # 9. -> Combine the first sentence, the middle body and the last sentence to form "The_Summary"
    The_Summary = Constants.SUMMARY(firstSentence, combined_summary, lastSentence)
    return The_Summary

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
    the_summary = Words.combine_words(final_list)
    return the_summary