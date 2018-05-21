import json
from pprint import pprint

with open('Tests/test_6/urls.json', 'r', encoding="utf8") as json_file:
    urls = json.load(json_file)
pprint(urls)

for index, articles in enumerate(urls):
    articles['id'] = index
pprint(urls)

with open('Tests/test_6/urls.json', 'w+', encoding="utf8") as file:
    json.dump(urls, file, indent=2, ensure_ascii=False)
