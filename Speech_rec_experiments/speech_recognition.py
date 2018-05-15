import speech_recognition as sr
from pymystem3 import Mystem

recognizer = sr.Recognizer()
mystem = Mystem()

with sr.Microphone() as source:
    print("Скажите что-нибудь")
    audio = recognizer.listen(source)

try:
    answer = recognizer.recognize_google(audio, language="ru-RU")
    result = mystem.analyze(answer)
    print('Фраза: ', answer)
    print('Глаголы:', end=' ')

    for index in range(len(result)):
        if result[index].get('analysis'):
            dic = result[index].get('analysis')[0]
            if 'V' in dic.get('gr'):
                print(result[index].get('text'), end='; ')

    if 'привет'.lower() in answer.lower():
        print('\nКстати, и тебе привет!')


except sr.UnknownValueError:
    print("Робот не расслышал фразу")
except sr.RequestError as e:
    print("Ошибка сервиса; {0}".format(e))
