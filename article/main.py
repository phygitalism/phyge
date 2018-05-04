import pandas as pd
from ArticleFetcher import ArticleFetcher
from ArticleSerializer import ArticleSerializer
from BagOfWordsModel import BagOfWordsModel
from CreateSearchQuery import CreateSearchQuery


def filtred_download_urls(urls_to_download, existing_urls):
    return [x for x in urls_to_download if x not in existing_urls]


def create_df_words(article):
    df_words_in_doc = pd.DataFrame()
    for i in range(0, len(article)):
        df_words_in_doc[i] = pd.Series(article[i].normalized_words)
        df_words_in_doc.to_csv('value.csv', index=False, encoding='utf8')
    return df_words_in_doc


def create_uci(article, name_module, OUT_FOLDER):
    dict_kek = {}
    for i in range(0, len(article)):
        dict_kek.update({i: str(article[i].normalized_words)})
    bag_of_words = BagOfWordsModel(dict_kek)
    bag_of_words.to_uci(model_name=name_module, save_folder=OUT_FOLDER)


if __name__ == '__main__':
    data_url = pd.read_csv('url_test.csv')
    urls_to_download = data_url.iloc[0:2, 0]
    saved_articles = ArticleSerializer.deserialize()
    existing_urls = [article.downloaded_from_url for article in saved_articles]

    filtred_urls = filtred_download_urls(urls_to_download, existing_urls)
    print('New url:\n', filtred_urls)

    article_fetcher = ArticleFetcher(filtred_urls)
    downloaded_articles = article_fetcher.fetch()

    downloaded_articles += saved_articles
    article_serializer = ArticleSerializer.serialize(downloaded_articles)
    desirialized_articles = ArticleSerializer.deserialize()

    print('\nTitle parsed article and url:')
    for i in range(0, len(desirialized_articles)):
        print(desirialized_articles[i], desirialized_articles[i].downloaded_from_url)

    print('\nCreate dataframe all words (value.csv)')
    df_words_in_doc = create_df_words(desirialized_articles)

    def view_value_counts(size_of_head):
        for i in range(0, len(df_words_in_doc.columns)):
            print('url №', i, '\n', df_words_in_doc.iloc[:, i].value_counts().head(size_of_head))
    print('\nView value counts:')
    view_value_counts(size_of_head=10)

    # CREATE UCI
    save_folder = 'test_2_urls'
    text = 'ОС Windows долгое время попрекали за медлительность её файловых операций и медленное создание процессов. А почему бы не попробовать сделать их ещё более медленными? Эта статья покажет способы замедления файловых операций в Windows примерно в 10 раз от их нормальной скорости (или даже больше), причём способы эти практически не поддаются отслеживанию обычным пользователем.'

    create_uci(desirialized_articles, name_module='article', OUT_FOLDER=save_folder)
    print('\nOK Create uci from Article (to', save_folder, '):')

    create_seatch_query = CreateSearchQuery(text)
    best_kek = {'test_text': str(create_seatch_query.query_normalize)}
    bag_of_words = BagOfWordsModel(best_kek)
    bag_of_words.to_uci(model_name='query', save_folder=save_folder)
    print('OK Create uci from Query (to', save_folder, '):')

