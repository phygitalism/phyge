import os.path
import json

from Models.PhygeArticle import PhyArticle


class ArticleSerializer:

    @classmethod
    def serialize(cls, objects: list, path):
        serialized = list(map(lambda x: x.serialized(), objects))

        with open(path, 'w+', encoding="utf8") as file:
            s = json.dumps(serialized, indent=2, ensure_ascii=False)
            file.write(s)

    @classmethod
    def deserialize(cls, path) -> [PhyArticle]:
        if not os.path.isfile(path):
            return list()

        with open(path, 'r', encoding="utf8") as file:
            articles = json.load(file)
            return [PhyArticle(obj) for obj in articles]
