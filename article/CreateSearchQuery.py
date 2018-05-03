import re
from nltk.corpus import stopwords
import pymorphy2
from BagOfWordsModel import BagOfWordsModel

text = 'Вызывая большую функцию и используя результат несколько раз, сохраните результат в переменной вместо того, чтобы постоянно вызывать данную функцию. Хорошо спроектированная функция имеет следующие характеристики. Используйте параметры, чтобы отправлять информацию из функции или когда функции нужно возвратить несколько значений. Отправляя объект в функцию как параметр, вы должны передавать его по ссылке, так как если он будет передан как значение, то будет скопирован весь объект. Копирование объектов требует больших затрат памяти.'
tokens = re.sub('[^\w]', ' ', text).split()
text_tokens = list(map(str.lower, tokens))
russian_words = re.compile('[А-Яа-я]+').findall(' '.join(text_tokens))

morph = pymorphy2.MorphAnalyzer()
russian_words_normal = list(map(lambda x: morph.parse(x)[0].normal_form, russian_words))
filtered_tokens = list(filter(lambda x: x not in stopwords.words('russian') and len(x) > 1, russian_words_normal))


print(filtered_tokens)
best_kek = {}
best_kek.update({'test_text': str(filtered_tokens)})
bag_of_words = BagOfWordsModel(best_kek)