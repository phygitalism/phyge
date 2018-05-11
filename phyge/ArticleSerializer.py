import os.path
import json

from Models.PhyArticle import PhyArticle


class ArticleSerializer:

    @classmethod
    def serialize(cls, objects: list, path):
        serialized = list(map(lambda x: x.serialized(), objects))

        with open(path, 'w+') as file:
            s = json.dumps(serialized)
            file.write(s)

    @classmethod
    def deserialize(cls, path) -> [PhyArticle]:
        if not os.path.isfile(path):
            return list()

        with open(path, 'r') as file:
            articles = json.load(file)
            return [PhyArticle(obj) for obj in articles]
