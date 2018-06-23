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

    testCasePath = str.format('{0}/test_{1}', testsDir, currentTestKey)
    urlsPath = os.path.join(testCasePath, urlsFileKey)
    queriesPath = os.path.join(testCasePath, queriesFileKey)

    tmpPath = testCasePath + '/tmp/'

    articlesPath = tmpPath + articlesFileKey
    valuesPath = tmpPath + valuesFileKey
    urlsStatusPath = tmpPath + urlsStatusFileKey
    lsiPath = tmpPath + modelLsiKey
    ldaPath = tmpPath + modelLdaKey
    w2vPath = tmpPath + modelW2vKey
    dctPath = tmpPath + dctFileKey

    resourcesDir = 'Resources'
    stopwordsDir = 'stopwords'
    ruStopwordsKey = 'russian'
    enStopwordsKey = 'russian_english'
    ruStopwordsPath = os.path.join(resourcesDir, stopwordsDir, ruStopwordsKey)
    enStopwordsPath = os.path.join(resourcesDir, stopwordsDir, enStopwordsKey)


