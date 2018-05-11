
class PhyVariables:
    testsPath = 'Tests'

    urlsFileKey = 'urls.csv'
    articlesFileKey = 'articles.json'
    queriesFileKey = 'queries.json'
    valuesFileKey = 'values.csv'

    def __init__(self):
        self.ulrs_key = 'urls_three_topic.csv' #'url_test.csv'
        self.save_folder_key = 'test_3_topis_20urls'
        self.articles_json_key = 'articles.json'
        self.query_json_key = 'query.json'

        self.docword_articles_key = '/docword.articles.txt'
        self.vocab_articles_key = '/vocab.articles.txt'
        self.docword_query_key = '/docword.query.txt'
        self.vocab_query_key = '/vocab.query.txt'
        self.model_name_key = '/ldamodel_xkcd_1'
