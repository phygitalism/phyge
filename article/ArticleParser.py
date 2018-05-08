import pandas as pd
from PhyArticle import PhyArticle
from BagOfWordsModel import BagOfWordsModel


class ArticleParser:
    def __init__(self, url=pd.DataFrame):
        self.url = url
        self.count_doc = len(self.url)
        print('count URL: ', self.count_doc)
        self.article = self.parse()

    def parse(self, normalized_words, ):
            self.url.loc[i, 'test'] = 1 if len(normalized_words) > 0 else 0
            print(i + 2, ' url test: ', self.url.loc[i, 'test'], '\n')  # +2 to match the numbering in a file url.csv
        self.url.to_csv('test_data.csv', index=False)

        return article


0

if __name__ == '__main__':
    article_parser = ArticleParser(saved_articles)
    article_parser.create_uci(count_doc)
