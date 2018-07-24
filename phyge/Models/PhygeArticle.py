

class PhyArticle:
    id_key = 'serial_id'
    title_key = 'title'
    text_key = 'text'
    source_key = 'source'
    language_key = 'lang'
    normalized_words_key = 'normalized_words'

    def __init__(self, obj=None):
        if obj is None:
            obj = dict()

        self.id = obj.get(self.id_key)
        self.title = obj.get(self.title_key)
        self.text = obj.get(self.text_key)
        self.source = obj.get(self.source_key)
        self.language = obj.get(self.language_key, '')
        self.normalized_words = obj.get(self.normalized_words_key, list())

    def serialize(self):
        return {
            self.id_key: self.id,
            self.title_key: self.title,
            self.text_key: self.text,
            self.source_key: self.source,
            self.language_key: self.language,
            self.normalized_words_key: self.normalized_words
        }

    def __str__(self):
        return self.title
