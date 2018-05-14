import time
from pprint import pprint
from gensim import corpora, models, similarities
from Models.PhygeArticle import PhyArticle
from Storage import Storage

if __name__ == '__main__':

    def find_article(model_corpus, query_vec):
        start_time = time.time()
        index = similarities.MatrixSimilarity(model_corpus)
        sims = index[query_vec]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        print('answer', sims[0:5])
        print('answer time:', round((time.time() - start_time), 3), 's')
        articles: [PhyArticle] = test_case.articles
        result = list()
        for index, similarity in sims[0:5]:
            article_similarity = {'title': articles[index].title,
                                  'url': articles[index].downloaded_from_url,
                                  'similarity': similarity}
            result.append(article_similarity)
        return result

    def comparison_answer(model_answer):
        if model_answer['url'] == true_answer:
            print('Article found correctly!')
        else:
            print('Article found NOT correctly! the first five articles:')


    storage = Storage()
    test_case = storage.load_test_case(1)
    test_case.setup()
    df = test_case.values
    query_normalize = test_case.queries[0].normalized_words

    true_answer = test_case.queries[0].url
    print('TRUE URL = ', true_answer, ', Title:', test_case.queries[0].title)

    documents = []
    for columns in df.columns:
        documents.append(df[columns].dropna().tolist())
    dct = corpora.Dictionary(documents)
    vec_bow_query = dct.doc2bow(query_normalize)
    # dct.save(path + '/deerwester.dict')
    corpus = [dct.doc2bow(doc) for doc in documents]
    # corpora.MmCorpus.serialize(path + '/deerwester.mm', corpus)  # store to disk, for later use

    print('\nLSI model:')
    start_time_LSI = time.time()
    lsi = models.LsiModel(corpus, id2word=dct, num_topics=100)
    print('Learning time:', round((time.time() - start_time_LSI), 3), 's')
    lsi_answer = find_article(lsi[corpus], lsi[vec_bow_query])
    pprint(lsi_answer[0:2])
    comparison_answer(lsi_answer[0])

    print('\nLDA model:')
    start_time_LDA = time.time()
    lda = models.ldamodel.LdaModel(corpus, id2word=dct, num_topics=100, passes=20)
    print('Learning time:', round((time.time() - start_time_LDA), 3), 's')
    lda_answer = find_article(lda[corpus], lda[vec_bow_query])
    pprint(lda_answer[0:2])
    comparison_answer(lda_answer[0])

