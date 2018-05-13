import pandas as pd
import time
from gensim import corpora, models, similarities
from Models.PhygeVariables import PhyVariables
from Storage import Storage

if __name__ == '__main__':

    storage = Storage()
    test_case = storage.load_test_case(1)
    test_case.setup()

    df = pd.read_csv(test_case.path + '/' + PhyVariables.valuesFileKey)
    query_normalize = str(test_case.queries[0]).split()

    documents = []
    for columns in df.columns:
        documents.append(df[columns].dropna().tolist())
    dct = corpora.Dictionary(documents)
    vec_bow_query = dct.doc2bow(query_normalize)
    # dct.save(path + '/deerwester.dict')
    corpus = [dct.doc2bow(doc) for doc in documents]
    # corpora.MmCorpus.serialize(path + '/deerwester.mm', corpus)  # store to disk, for later use

    start_time_LSI = time.time()
    lsi = models.LsiModel(corpus, id2word=dct, num_topics=100)
    print('LSI model:')
    print('Learning time:', round((time.time() - start_time_LSI), 3), 's')
    start_time_LSI = time.time()
    vec_lsi = lsi[vec_bow_query]  # convert the query to LSI space
    index = similarities.MatrixSimilarity(lsi[corpus])
    sims = index[vec_lsi]  # perform a similarity query against the corpus
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    print('answer', sims[0:5])  # print sorted (document number, similarity score) 2-tuples
    print('answer time:', round((time.time() - start_time_LSI), 3), 's')

    start_time_LDA = time.time()
    lda = models.ldamodel.LdaModel(corpus, id2word=dct, num_topics=100, passes=20)
    print('\nLDA model:')
    print('Learning time:', round((time.time() - start_time_LDA), 3), 's')
    start_time_LDA = time.time()
    vec_lda = lda[vec_bow_query]
    index = similarities.MatrixSimilarity(lda[corpus])
    sims = index[vec_lda]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    print('answer', sims[0:5])  # print sorted (document number, similarity score) 2-tuples
    print('time:', round((time.time() - start_time_LDA), 3), 's')