
from Models.Query import Query

from TematicModels import BaseModel


class SearchEngine:
    def __init__(self, model: BaseModel):
        self.model = model

    def find_article(self, query: Query, amount=5):
        return self.model.perform_search(normalized_query=query.normalized_words)


if __name__ == '__main__':
    pass
