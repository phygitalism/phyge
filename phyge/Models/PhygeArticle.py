from readability.readability import Document
from bs4 import BeautifulSoup

from TextNormalizer import TextNormalizer

#from googletrans import Translator

class PhyArticle:
    def __init__(self, obj=None):
        if obj is None:
            obj = dict()

        self.downloaded_from_url = obj.get('url', '')
        self.title = obj.get('title', '')
        self.readable_html = obj.get('readable_html', '')
        self.text = obj.get('text', '')
        self.normalized_words = obj.get('normalized_words', list())
        self.language = obj.get('language', '')

    def deserialize_from(self, obj: dict):
        return PhyArticle(obj)

    def __str__(self):
        return self.title

    def transform(self, article_html, downloaded_from_url, language):
        self.downloaded_from_url = downloaded_from_url
        self.language = language
        self.readable_html = Document(article_html.html).summary()
        self.title = Document(article_html.html).short_title()
        self.text = self.__transform_to_single_line(self.readable_html)

        #self.language = Translator().detect(self.text).lang
        #print('language is', self.language)

        if self.language == 'en':
            try:
                from googletrans import Translator
                print('Translate')
                if len(self.text) < 5000:
                    self.text = Translator().translate(self.text, dest='ru').text
                else:
                    from math import ceil
                    block_number = ceil(len(self.text) / 5000) # Определяем количество блоков, которые будем переводить
                    translated_text = ''
                    for i in range(block_number):
                        translated_text += Translator().translate(self.text[5000*i:5000*(i+1)], dest='ru').text
                    self.text = translated_text
            except:
                print('Error while translating')
                with open('out_info.txt', 'a') as info:
                    info.write("Cann't be translated " + self.title + "\n")

        self.normalized_words = TextNormalizer.normalize(self.text)


    def __transform_to_single_line(self, raw_html):
        soup = BeautifulSoup(raw_html, "lxml")
        return str(soup.findAll(text=True)).replace("\\n", "").replace("\\r", "").replace('\\xa0', '').replace('\'', '')

    def serialized(self):
        return {'url': self.downloaded_from_url,
                'title': self.title,
                'text': self.text,
                'language': self.language,
                'normalized_words': self.normalized_words}
