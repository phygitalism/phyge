# План доклада

- структура ML (отличие классических алгоритмов ML, нейронных сетей, глубинного обучения)
- подготовка к обучению модели
  - подготовка данных
  - выбор алгоритма
- виды алгоритмов, задачи какие решают (Женя)
  - классификация
  - класторизация 
  - регрессия (прогнозирование, рекомендации */упоминуть про кентавров/*)
  - понижение размерности
- как оценить результат *важно*
- основные бибилиотеки/рассмотренные инстуременты (Саша)
- интересные примеры
  - [OpenAI](https://www.imena.ua/blog/inside-openai/), [AIGym](https://habrahabr.ru/company/newprolab/blog/343834/), GAN - [Генеративные модели от OpenAI](https://habrahabr.ru/company/wunderfund/blog/334568/) 
  - [CoreML](https://habrahabr.ru/company/mobileup/blog/332500/) от Apple, [Apple Machine Learning Journal](https://machinelearning.apple.com)
    - [Learning with Privacy at Scale](https://machinelearning.apple.com/2017/12/06/learning-with-privacy-at-scale.html)

*Обязательно список ресурсов в конце, сохраняйте ссылки на статьи, можно хаотично*

**Алгоритмы из либы Sklearn:**

1. LogisticRegression - логическая регрессия
2. SGDClassifier - стохастический градиентный спуск
3. MLPClassifier - многоуровневый перцептрон
4. RandomForestClassifier - случайные леса
5. GradientBoostingClassifier - [User Guide](http://scikit-learn.org/stable/modules/ensemble.html#gradient-boosting)
6. DecisionTreeClassifier - дерево принятий решений
7. SVC - метод опорных векторов (?) 

**На примере Титаника:**   
*accuracy, class*   
0.8101           LogisticRegression   
0.7765               SGDClassifier   
0.8156               MLPClassifier   
0.8212      RandomForestClassifier   
0.8156  GradientBoostingClassifier   
0.8156      DecisionTreeClassifier   
0.7877                         SVC   
