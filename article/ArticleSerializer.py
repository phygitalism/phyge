import json

from PhyArticle import PhyArticle
from PhyVariables import PhyVariables

class ArticleSerializer:
    phy_var = PhyVariables()
    path = phy_var.articles_json_key

    @classmethod
    def serialize(cls, objects: list):
        serialized = list(map(lambda x: x.serialized(), objects))

        with open(cls.path, 'w+') as file:
            s = json.dumps(serialized)
            file.write(s)

    @classmethod
    def deserialize(cls) -> [PhyArticle]:
        # check file exist, if not return empty list

        with open(cls.path, 'r') as file:
            articles = json.load(file)
            return [PhyArticle(obj) for obj in articles]
