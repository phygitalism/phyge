import json
import time

from pprint import pprint
from SearchEngine import SearchEngine
from Models.Query import BaseQuery

from DatabaseSeeder import DatabaseSeeder
from DBController import DBController

from Storage import Storage
from PhygeVariables import PhyVariables
import os

search_engine: SearchEngine = None


def get_queries(path) -> [BaseQuery]:
    if not os.path.isfile(path):
        return list()
    with open(path, 'r', encoding='utf8') as json_file:
        data_queries = json.load(json_file)
        return [BaseQuery(obj) for obj in data_queries]


def run_search(path, result_path, amount=1):
    search_results = []
    query_list = get_queries(path)
    for query in query_list:
        search_results.append(search_article(query, amount))
    save_results(result_path, search_results, query_list)


def search_article(query, amount):
    global search_engine
    start_time = time.time()
    search_results = search_engine.find_article(query, amount=amount)
    answer_time = round((time.time() - start_time), 3)
    # search_results['search_time'] = answer_time

    print('search_results')
    pprint(search_results)
    return search_results


def save_results(result_path, search_results, query_list):
    wrong_ids = dict()
    with open(result_path, 'w', encoding='utf8') as file:
        output_answer = []
        for i, answer in enumerate(search_results):
            for model_name in answer.keys():
                true_sourse = query_list[i].source
                # found_title = answer[model_name][0]['title']
                found_sourse = answer[model_name][0]['source']
                if true_sourse != found_sourse:
                    if model_name not in wrong_ids.keys():
                        wrong_ids[model_name] = [("true", "found"), (true_sourse, found_sourse)]
                    else:
                        wrong_ids[model_name].append((true_sourse, found_sourse))
                output_answer.append(dict(true_sourse=true_sourse, sourse=found_sourse, model=model_name,
                                          title=answer[model_name][0]['title'],
                                          similarity=answer[model_name][0]['similarity']))
        file.write(json.dumps(output_answer, indent=2, ensure_ascii=False))
        file.write(json.dumps(wrong_ids, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    log_of_result = []

    if len(DBController.get_all_documents()) == 0:
        print('Seeding database...')
        DatabaseSeeder.seed()

    lsi = Storage.load_model('out/lsi', 'phyge', 'lsi')

    lda = Storage.load_model('out/lda', 'phyge', 'lda')
    d2v = Storage.load_model('out/d2v', 'phyge', 'd2v')
    fast_text = Storage.load_model('out/fast_text', 'phyge', 'ft')
    search_engine = SearchEngine(models=[fast_text, d2v, lda, lsi])
    test_path = os.path.join(PhyVariables.testsDir, 'test_' + str(PhyVariables.queriesId))
    run_search(os.path.join(test_path, PhyVariables.queriesFileName),
               os.path.join(test_path, PhyVariables.answersFileName), 1)
    # run_search('Resources/pdf_articles.json','Resources/answers.json',1)
