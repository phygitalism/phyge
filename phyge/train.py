from DBController import DBController
from DatabaseSeeder import DatabaseSeeder
from Models.TrainingSample import TrainingSample
from TematicModels import LsiModel, LdaModel

from Storage import Storage

if __name__ == "__main__":

    if len(DBController.get_all_articles()) == 0:
        print('Seeding database...')
        DatabaseSeeder.seed()

    articles = DBController.get_all_articles()
    testing_sample = TrainingSample(articles)

    lsi = LsiModel(model_name='phyge')
    lda = LdaModel(model_name='phyge')

    lsi.train_model(testing_sample)
    lda.train_model(testing_sample)

    Storage.save_model(lsi, path='out/lsi')
    Storage.save_model(lda, path='out/lda')
