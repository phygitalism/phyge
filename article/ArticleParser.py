import pandas as pd
from PhyArticle import PhyArticle
from BagOfWordsModel import BagOfWordsModel


class ArticleParser:
    def __init__(self, data_url):
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

    def create_uci(self, count_doc):
        for i in range(0, count_doc):
            self.dict_kek.update({i: str(self.article.normalized_words)})
        bag_of_words = BagOfWordsModel(self.dict_kek)
        bag_of_words.to_uci()
0

if __name__ == '__main__':
    article_parser = ArticleParser(saved_articles)
    article_parser.create_uci(count_doc)
