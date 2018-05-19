
from Storage import Storage


if __name__ == '__main__':
    storage = Storage(test_case_id=4)
    test_case = storage.load_test_case()
    test_case.setup()
    print('\nTitle parsed article and url:')
    for article in test_case.articles:
        print(str.format('{0} [{1}]', article, article.downloaded_from_url))

    for index, query in enumerate(test_case.queries, start=1):
        print(str.format('Query #{0}:\n{1}', index, query))
