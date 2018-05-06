from gensim import corpora, models
from scipy import spatial
from PhyVariables import PhyVariables

phy_var = PhyVariables()
path = phy_var.save_folder_key
data = corpora.UciCorpus(path + phy_var.docword_articles_key, path + phy_var.vocab_articles_key)
dictionary = data.create_dictionary()

num_topics = 2
# train model
ldamodel = models.ldamodel.LdaModel(data, id2word=dictionary, num_topics=num_topics, passes=50, alpha=1.25, eta=1.25)
ldamodel.save(path + phy_var.model_name_key)
# ldamodel = models.ldamodel.LdaModel.load(path+phy_var.model_name_key)

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

perplexity = ldamodel.log_perplexity(list(data))
print(2 ** (-perplexity))

perp = ldamodel.bound(data)
2 ** (-perp / float(87409))

data2 = corpora.UciCorpus(path + phy_var.docword_query_key, path + phy_var.vocab_query_key)


def to_vec(x):
    kl = np.zeros(num_topics)
    # kl = [.0,.0,.0,.0,.0,.0,.0,.0,.0,.0]
    for i in range(len(x)):
        j = x[i][0]
        kl[j] = x[i][1]
    return np.array(kl)


P_tema_query = ldamodel.get_document_topics(list(data2)[0])
print('\nраспределение тем для запроса: \n', P_tema_query)
P_tema_query_vec = []
for i in range(0, len(P_tema_query)):
    P_tema_query_vec.append(P_tema_query[i][1])
print('\nраспределение тем для запроса в виде вектора:')
print(P_tema_query_vec)

print('распределение url №:')

cos_sum = []
for i in range(1):
    P_tema_articles = ldamodel.get_document_topics(list(data)[i])
    P_tema_articles_vec = to_vec(P_tema_articles)
    # print(i + 2, P_tema_articles_vec)

    print('косинус: ', i)
    sim = 1 - spatial.distance.cosine(P_tema_articles_vec, P_tema_query_vec)
    cos_sum.append(sim)
print(cos_sum)
print(cos_sum.index(max(cos_sum)) + 1)
