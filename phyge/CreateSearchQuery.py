import re
from nltk.corpus import stopwords
import pymorphy2
import json
from PhyVariables import PhyVariables


class CreateSearchQuery:
    def __init__(self, path_query=PhyVariables().query_json_key):
        self.path_query = path_query
        self.text_normalize = self.create_uci()

    def load_query(self):
        with open(self.path_query, 'r', encoding='utf8') as data_file:
            text_query = json.load(data_file)
        return text_query['text']

    def create_uci(self):
        text = self.load_query()
        tokens = re.sub('[^\w]', ' ', text).split()
        text_tokens = list(map(str.lower, tokens))
        russian_words = re.compile('[А-Яа-я]+').findall(' '.join(text_tokens))
        morph = pymorphy2.MorphAnalyzer()
        russian_words_normal = list(map(lambda x: morph.parse(x)[0].normal_form, russian_words))
        return list(filter(lambda x: x not in stopwords.words('russian') and len(x) > 1, russian_words_normal))


if __name__ == '__main__':
    create_search_query = CreateSearchQuery()
    print(create_search_query.text_normalize)
