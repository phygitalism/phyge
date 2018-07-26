import os


class PhyVariables:
    testsDir = 'Tests'
    articlesIdFileName = 'articles_id.json'

    resourcesDir = 'Resources'
    stopwordsDir = 'stopwords'
    ruStopwordsKey = 'russian'
    enStopwordsKey = 'russian_english'
    ruStopwordsPath = os.path.join(resourcesDir, stopwordsDir, ruStopwordsKey)
    enStopwordsPath = os.path.join(resourcesDir, stopwordsDir, enStopwordsKey)


