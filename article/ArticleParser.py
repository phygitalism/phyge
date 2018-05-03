import pandas as pd
from PhyArticle import PhyArticle
from BagOfWordsModel import BagOfWordsModel


class ArticleParser:
    def __init__(self, list_url_csv_key):
        self.data_url = pd.read_csv(list_url_csv_key)
        self.count_doc = len(self.data_url)
        print('count URL: ', self.count_doc)

        self.df_words_in_doc = pd.DataFrame()
        self.dict_kek = {}
        self.article = self.parse()

    def parse(self):
        for i in range(0, self.count_doc):
            current_url = self.data_url.iloc[i, 0]
            article = PhyArticle(current_url)
            self.data_url.loc[i, 'test'] = 1 if len(article.normalized_words) > 0 else 0
            print(i+2, ' url test: ', self.data_url.loc[i, 'test'], '\n') #+2 to match the numbering in a file url.csv
        self.data_url.to_csv(list_url_csv_key, index=False)
        return article

    def create_df_words(self):
        for i in range(0, self.count_doc):
            self.df_words_in_doc[i] = pd.Series(self.article.normalized_words)
            self.df_words_in_doc.to_csv('value.csv', index=False)
            # print(self.df_words_in_doc[i].value_counts())

    def create_uci(self):
        for i in range(0, self.count_doc):
            self.dict_kek.update({i: str(self.article.normalized_words)})
        bag_of_words = BagOfWordsModel(self.dict_kek)
        bag_of_words.to_uci()
0

if __name__ == '__main__':
    list_url_csv_key = 'url_test.csv'
    article_parser = ArticleParser(list_url_csv_key)

    article_parser.create_df_words()
    for i in range(0, article_parser.count_doc):
        print(i+2, 'value counts: \n', article_parser.df_words_in_doc[i].value_counts(), '\n____')
    article_parser.create_uci()
