from Models.BagOfWordsModel import BagOfWordsModel


class Query:
    idKey = 'id'
    urlKey = 'url'
    textKey = 'text'
    titleKey = 'title'
    summaryKey = 'summary'

    def __init__(self, obj: dict):
        self.id = obj.get(self.idKey, None)
        self.url = obj.get(self.urlKey, None)
        self.text = obj.get(self.textKey, None)
        self.title = obj.get(self.titleKey, None)
        self.summary = obj.get(self.summaryKey, None)

    def uci_representation(self, path):
        bag_of_words = BagOfWordsModel({self.id: self.text})
        bag_of_words.to_uci(model_name='query', save_folder=path+'/uci')
