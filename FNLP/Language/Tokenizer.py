from F import LIST
from FNLP.Language import Sentences
from FNLP.Language import Words


def tokenize_content_into_sentences(content):
    """ Split a large string into sentences """
    sentences = Sentences.to_sentences(content)
    sentences = [x.replace('\n', '') for x in sentences if len(x) > 10]
    return sentences

def score_complete_tokenization(tokenization: dict):
    result = {}
    for key in tokenization.keys():
        token_list = tokenization[key]
        result[key] = Words.score_words(token_list)
    return result

# @Ext.safe_args
def complete_tokenization_v2(*content, toList=True):
    """ PUBLIC """
    content = LIST.flatten(content)
    toStr = LIST.to_str(content)
    tokens = Words.to_words_v1(toStr)
    bi_grams = Words.to_x_grams(tokens, 2)
    tri_grams = Words.to_x_grams(tokens, 3)
    quad_grams = Words.to_x_grams(tokens, 4)
    if toList:
        return tokens + bi_grams + tri_grams + quad_grams
    else:
        return {"tokens": tokens, "bi_grams": bi_grams, "tri_grams": tri_grams, "quad_grams": quad_grams}
