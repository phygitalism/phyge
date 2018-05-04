import re
from nltk.corpus import stopwords
import pymorphy2


class CreateSearchQuery:
    def __init__(self, text=str):
        self.text = text
        self.query_normalize = self.create_uci()

    def create_uci(self):
        tokens = re.sub('[^\w]', ' ', self.text).split()
        text_tokens = list(map(str.lower, tokens))
        russian_words = re.compile('[А-Яа-я]+').findall(' '.join(text_tokens))
        morph = pymorphy2.MorphAnalyzer()
        russian_words_normal = list(map(lambda x: morph.parse(x)[0].normal_form, russian_words))
        return list(filter(lambda x: x not in stopwords.words('russian') and len(x) > 1, russian_words_normal))


if __name__ == '__main__':
    text_normalize = 'ОС Windows долгое время попрекали за медлительность её файловых операций и медленное создание процессов. А почему бы не попробовать сделать их ещё более медленными? Эта статья покажет способы замедления файловых операций в Windows примерно в 10 раз от их нормальной скорости (или даже больше), причём способы эти практически не поддаются отслеживанию обычным пользователем.'
    create_search_query = CreateSearchQuery(text_normalize)
