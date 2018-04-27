from newspaper import Article
from readability.readability import Document
from bs4 import BeautifulSoup
import re
from nltk.corpus import stopwords
import pymorphy2
import numpy as np
import matplotlib.pyplot as plt
import nltk
import pandas as pd

data_url = pd.read_csv('url_test.csv')
pd.set_option('display.expand_frame_rep', False)
print(data_url)
current_url = data_url.iloc[10, 0]
print('\n current url ', current_url)


def fetch_article(url):
    article = Article(url, language='ru')
    article.download()
    summary = Document(article.html).summary()
    readable_title = Document(article.html).short_title()

    return readable_title, summary


def tokenize_text(text):
    tokens = re.sub('[^\w]', ' ', text).split()
    return list(map(str.lower, tokens))


def normalize_tokens(tokens):
    morph = pymorphy2.MorphAnalyzer()
    return list(map(lambda x: morph.parse(x)[0].normal_form, tokens))


def transform_to_single_line(summary):
    soup = BeautifulSoup(summary, "lxml")
    return str(soup.findAll(text=True)).replace("\\n", "").replace("\\r", "")


title, summary = fetch_article(url=str(current_url))
text = transform_to_single_line(summary)
text_tokens = tokenize_text(text)

russian_words = re.compile('[А-Яа-я]+').findall(' '.join(text_tokens))
print('russian words', russian_words, len(russian_words))

filtered_tokens = list(filter(lambda x: x not in stopwords.words('russian') and len(x) > 1, russian_words))
print('filtered_tokens', filtered_tokens, len(filtered_tokens))

normalized_tokens = normalize_tokens(filtered_tokens)
print('normalized_tokens', normalized_tokens, len(normalized_tokens))


# bg = list(nltk.bigrams(all_words))
# bgfd = nltk.FreqDist(bg)
# bgfd.most_common(20)
