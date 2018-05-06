from gensim import corpora, models
from scipy import spatial
from PhyVariables import PhyVariables
import numpy as np


# Косинусное расстояние - чем больше, тем лучше
def cos(x, y):
    return x.dot(y) / (np.sqrt(x.dot(x)) * np.sqrt(y.dot(y)))


def to_vec(x):
    kl = np.zeros(number_of_topics)
    # kl = [.0,.0,.0,.0,.0,.0,.0,.0,.0,.0]
    for i in range(len(x)):
        j = x[i][0]
        kl[j] = x[i][1]
    return np.array(kl)


def print_top_words():
    all_words = []
    for i in range(number_of_topics):
        rus_words = []
        words = ldamodel.show_topic(i, 10)
        words = np.take(words, [0], axis=1)
        for w in words:
            rus_words.append(w[0].decode('utf8'))
        all_words.append(rus_words)

    for i, w in enumerate(all_words):
        print("тема", i, ":", w)


def calculate_perplexity(model):
    model.log_perplexity(list(data))
    perp = ldamodel.bound(data)
    return 2 ** (-perp / float(87409))


if __name__ == '__main__':

    phy_var = PhyVariables()
    path = phy_var.save_folder_key
    data = corpora.UciCorpus(path + phy_var.docword_articles_key, path + phy_var.vocab_articles_key)
    dictionary = data.create_dictionary()

    number_of_topics = 2
    ldamodel = models.ldamodel.LdaModel(data, id2word=dictionary, num_topics=number_of_topics, passes=20, alpha=1.25, eta=1.25)
    ldamodel.save(path + phy_var.model_name_key)
    # Load model:
    # ldamodel = models.ldamodel.LdaModel.load(path+phy_var.model_name_key)

    print_top_words()

    perplexity = calculate_perplexity(ldamodel)
    print('\nperplexity = ', perplexity)

    data2 = corpora.UciCorpus(path + phy_var.docword_query_key, path + phy_var.vocab_query_key)

    P_tema_query = ldamodel.get_document_topics(list(data2)[0])
    print('\nраспределение тем для запроса: \n', P_tema_query)

    P_tema_query_vec = []
    for i in range(0, len(P_tema_query)):
        P_tema_query_vec.append(P_tema_query[i][1])
    print('\nраспределение тем для запроса в виде вектора:\n', P_tema_query_vec)

    cosines = []
    for i in range(2):
        P_tema_articles = ldamodel.get_document_topics(list(data)[i])
        P_tema_articles_vec = to_vec(P_tema_articles)
        sim = 1 - spatial.distance.cosine(P_tema_articles_vec, P_tema_query_vec)
        cosines.append(sim)

    print('\nкосинусы:', cosines)
    print('\nискомая статья - ', cosines.index(max(cosines)) + 1, 'я')
