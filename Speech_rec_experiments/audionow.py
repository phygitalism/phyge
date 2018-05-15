
from tornado import websocket
import tornado.ioloop
import speech_recognition as sr
import requests
import json


class EchoWebSocket(websocket.WebSocketHandler):
    def open(self):
        print "Websocket Opened"

    def on_message(self, message):
    	r = sr.Recognizer()
		audio = r.listen(message)

		try:
		    text = r.recognize_google(audio, language="en-US")
		except sr.UnknownValueError:
		    print("Робот не расслышал фразу")
		except sr.RequestError as e:
		    print("Ошибка сервиса; {0}".format(e))
		else:
			url = "https://poly.googleapis.com/v1/assets?key=AIzaSyCy9swQ5Bpq7fpAAXERwxQSoELh-KCZXa8&keywords="+text
			answerjson = requests.get(url)
			answerjson = json.loads(answerjson.json())
			answerjson = answerjson["assets"]
			answerjson = answerjson["0"]
			answerjson = answerjson["formats"]["0"]["root"]["url"]
			message = requests(answerjson)
			self.write_message(message.text)
		finally:
			print("ok")

    def on_close(self):
        print "Websocket closed"

application = tornado.web.Application([(r"/", EchoWebSocket),])

if __name__ == "__main__":
    application.listen(9000)
    tornado.ioloop.IOLoop.instance().start()