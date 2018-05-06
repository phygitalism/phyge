import pandas as pd
from ArticleFetcher import ArticleFetcher
from ArticleSerializer import ArticleSerializer
from CreateSearchQuery import CreateSearchQuery
from CreatedUci import CreatedUci
from PhyVariables import  PhyVariables
phy_var = PhyVariables()


def create_df_words(articles):
    columns = [pd.Series(article.normalized_words) for article in articles]
    pairs = zip(range(len(articles)), columns)
    data = dict((key, value) for key, value in pairs)

    df_words_in_doc = pd.DataFrame(data)
    df_words_in_doc.to_csv('value.csv', index=False, encoding='utf8')
    return df_words_in_doc


def load_data():
    data_url = pd.read_csv('url_test.csv')
    urls_to_download = data_url.iloc[0:2, 0]
    saved_articles = ArticleSerializer.deserialize()
    existing_urls = [article.downloaded_from_url for article in saved_articles]
    filtred_urls = [x for x in urls_to_download if x not in existing_urls]
    print('New url:\n', filtred_urls)

    article_fetcher = ArticleFetcher(filtred_urls)
    downloaded_articles = article_fetcher.fetch()

    downloaded_articles += saved_articles
    article_serializer = ArticleSerializer.serialize(downloaded_articles)
    return ArticleSerializer.deserialize()


if __name__ == '__main__':

    articles = load_data()

    print('\nTitle parsed article and url:')
    for article in articles:
        print(article, article.downloaded_from_url)

    print('\nCreate dataframe all words (value.csv)')
    df_words_in_doc = create_df_words(articles)


    def view_value_counts(size_of_head):
        for i in range(0, len(df_words_in_doc.columns)):
            print('url №', i, '\n', df_words_in_doc.iloc[:, i].value_counts().head(size_of_head))


    print('\nView value counts:')
    view_value_counts(size_of_head=10)

    # CREATE UCI
    print('\nCreate .uci:')
    save_folder = phy_var.save_folder_key

    text_query_normalize = CreateSearchQuery(path_query=phy_var.query_json_key).text_normalize
    uci_dict = CreatedUci(text_query=text_query_normalize, article=articles, save_folder=save_folder)
    uci_dict.create_uci(uci_dict.text_query, model_name='query')
    uci_dict.create_uci(uci_dict.text_article, model_name='articles')
