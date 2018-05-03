from gensim import corpora, models

data = corpora.UciCorpus('docword.bow.txt', 'vocab.bow.txt')
dictionary = data.create_dictionary()

num_topics = 7
# train model
ldamodel = models.ldamodel.LdaModel(data, id2word=dictionary, num_topics=num_topics, passes=20, alpha=1.25, eta=1.25)
ldamodel.save("ldamodel_xkcd")
ldamodel = models.ldamodel.LdaModel.load("ldamodel_xkcd")

import numpy as np

all_words = []
for i in range(num_topics):
    rus_words = []
    words = ldamodel.show_topic(i, 10)
    words = np.take(words, [0], axis=1)
    for w in words:
        rus_words.append(w[0].decode('utf8'))
    all_words.append(rus_words)

for i, w in enumerate(all_words):
    print("тема", i, ":", w)
