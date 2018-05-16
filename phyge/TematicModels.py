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

    TEST_NUMBER = 2
    TOPIC_NUMBER = 100

    storage = Storage()
    test_case = storage.load_test_case(TEST_NUMBER)
    test_case.setup()
    df = test_case.values

    documents = []
    for columns in df.columns:
        documents.append(df[columns].dropna().tolist())
    dct = corpora.Dictionary(documents)
    corpus = [dct.doc2bow(doc) for doc in documents]

    print('\nLSI model:')
    try:
        lsi = models.lsimodel.LsiModel.load('lsimodel')
    except:
        print('Модель не найдена')
        start_time_LSI = time.time()
        lsi = models.LsiModel(corpus, id2word=dct, num_topics=TOPIC_NUMBER)
        print('Learning time:', round((time.time() - start_time_LSI), 3), 's')
        lsi.save('lsimodel')

    print('\nLDA model:')
    try:
        lda = models.ldamodel.LdaModel.load('ldamodel')
    except:
        print('Модель не найдена')
        start_time_LDA = time.time()
        lda = models.ldamodel.LdaModel(corpus, id2word=dct, num_topics=TOPIC_NUMBER, passes=20)
        print('Learning time:', round((time.time() - start_time_LDA), 3), 's')
        lda.save('ldamodel')

    QUERY_NUMBER = len(test_case.queries)
    for i, query in enumerate(test_case.queries):
        print('QUERY NUMBER ', i + 1, '/', QUERY_NUMBER )
        query_normalize = query.normalized_words
        true_answer = query.url
        print('TRUE URL = ', query.url, ', Title:', query.title)


        vec_bow_query = dct.doc2bow(query_normalize)
        lsi_answer = find_article(lsi[corpus], lsi[vec_bow_query])
        pprint(lsi_answer[0:2])
        comparison_answer(lsi_answer[0])

        lda_answer = find_article(lda[corpus], lda[vec_bow_query])
        pprint(lda_answer[0:2])
        comparison_answer(lda_answer[0])
        print('------------------------------------\n')
        # dct.save(path + '/deerwester.dict')
        # corpora.MmCorpus.serialize(path + '/deerwester.mm', corpus)  # store to disk, for later use




