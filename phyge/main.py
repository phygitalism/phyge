from PhygeVariables import PhyVariables
from TestCase import TestCase

if __name__ == '__main__':
    test_case = TestCase(test_case_id=PhyVariables.currentTestKey)
    test_case.setup()
    print('\nTitle parsed article and url:')
    for article in test_case.articles:
        print(str.format('{0} [{1}]', article.title, article.url))

    for index, query in enumerate(test_case.queries, start=1):
        print(str.format('Query #{0}:\n{1}', index, query))
