class PhyArticle:
    def __init__(self, obj=None):
        if obj is None:
            obj = dict()

        self.url = obj.get('url', '')
        self.title = obj.get('title', '')
        self.text = obj.get('text', '')
        self.language = obj.get('language', '')
        self.normalized_words = obj.get('normalized_words', list())

    def serialize_to_phy(self, obj: dict):
        return PhyArticle(obj)

    def deserialize_to_dict(self):
        return {'url': self.url,
                'title': self.title,
                'text': self.text,
                'language': self.language,
                'normalized_words': self.normalized_words}

    def __str__(self):
        return self.title