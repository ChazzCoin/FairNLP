from F import DICT
from F.LOG import Log


def add_word_counts(scores_one:dict, scores_two:dict) -> dict:
    """ Add two dicts of word counts together
    brain_scores: {"word":, "count":}
    new_scores: { "word":, "count": }
    """
    result = {}

    """ Part 1. Preparing... """
    # All New Scored Words
    scores_one_list = []
    for word in scores_one.keys():
        scores_one_list.append(word)

    scores_two_list = []
    for word in scores_two.keys():
        scores_two_list.append(word)

    new_words = []
    for new_scored_word in scores_two_list:
        if new_scored_word in scores_one_list:
            continue
        new_words.append(new_scored_word)

    """ Part 2. Merging with Brain... """
    if scores_one_list:
        for scores_one_word in scores_one:
            scores_one_count = DICT.get(scores_one_word, scores_one, None)
            if scores_two.__contains__(scores_one_word):
                scores_two_count = DICT.get(scores_one_word, scores_two, None)
                new_score = int(scores_one_count) + int(scores_two_count)
                result[scores_one_word] = new_score
                continue
            result[scores_one_word] = scores_one_count

    """ Part 3. If new words, add them to brain... """
    if new_words:
        for new_word in new_words:
            result[new_word] = scores_two[new_word]

    return result