import os


class PhyVariables:
    testsDir = 'Tests'
    currentTestKey = 4
    urlsFileKey = 'urls.json'
    urlsStatusFileKey = 'urls.status.json'
    # urlsFileKey = 'en_slack_urls_clear.json'
    articlesFileKey = 'articles.json'
    queriesFileKey = 'queries.json'
    valuesFileKey = 'values.csv'
    modelLsiKey = 'phydge.lsi'
    modelLdaKey = 'phydge.lda'
    modelW2vKey = 'phyge.w2v'
    dctFileKey = 'deerwester.dict'

    resourcesDir = 'Resources'
    stopwordsDir = 'stopwords'
    ruStopwordsKey = 'russian'
    enStopwordsKey = 'russian_english'
    ruStopwordsPath = os.path.join(resourcesDir, stopwordsDir, ruStopwordsKey)
    enStopwordsPath = os.path.join(resourcesDir, stopwordsDir, enStopwordsKey)


