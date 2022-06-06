import os

STOPWORDS = os.path.join(os.path.dirname(__file__), 'stopwords.txt')

def get_resource(resource):
    """Uses generator to return next useragent in saved file
    """
    with open(resource, 'r') as f:
        words = [u.strip() for u in f.readlines()]
        return words

def get_stopwords():
    return get_resource(STOPWORDS)

if __name__ == '__main__':
    print(get_stopwords())