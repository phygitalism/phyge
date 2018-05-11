import re
import pymorphy2

from nltk.corpus import stopwords


class TextNormalizer:

    @classmethod
    def normalize(cls, text):
        text_tokens = cls.__tokenize_text(text)
        russian_words = re.compile('[А-Яа-я]+').findall(' '.join(text_tokens))
        russian_words = cls.__normalize_tokens(russian_words)
        return list(filter(lambda x: x not in stopwords.words('russian') and len(x) > 1, russian_words))

    @classmethod
    def __tokenize_text(cls, text):
        tokens = re.sub('[^\w]', ' ', text).split()
        return list(map(str.lower, tokens))

    @classmethod
    def __normalize_tokens(cls, tokens):
        morph = pymorphy2.MorphAnalyzer()
        return list(map(lambda x: morph.parse(x)[0].normal_form, tokens))
