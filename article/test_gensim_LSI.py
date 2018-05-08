import pandas as pd
from gensim import corpora, models, similarities
from PhyVariables import PhyVariables
from CreateSearchQuery import CreateSearchQuery

phy_var = PhyVariables()
path = phy_var.save_folder_key
create_search_query = CreateSearchQuery()
query_normalize = create_search_query.text_normalize

df = pd.read_csv('value.csv')

documents = []
for columns in df.columns:
    documents.append(df[columns].dropna().tolist())

dct = corpora.Dictionary(documents)
dct.save(path + '/deerwester.dict')
print(dct)

corpus = [dct.doc2bow(doc) for doc in documents]
corpora.MmCorpus.serialize(path + '/deerwester.mm', corpus)  # store to disk, for later use

lsi = models.LsiModel(corpus, id2word=dct, num_topics=2)

vec_bow = dct.doc2bow(query_normalize)
vec_lsi = lsi[vec_bow]  # convert the query to LSI space

index = similarities.MatrixSimilarity(lsi[corpus])
sims = index[vec_lsi]  # perform a similarity query against the corpus
sims = sorted(enumerate(sims), key=lambda item: -item[1])
print('answer ', sims[0])  # print sorted (document number, similarity score) 2-tuples
