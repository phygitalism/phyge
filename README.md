# MLX

## Instalation for Phyge
- В корне папки проекта Phyge лежат файлы для Docker'a    
- Запускаете приложение Docker от админа    
- В терминале переходите в папку с проектом    
- Собираете билд докера командой: ***$ docker build --no-cache -t phyge .***    
- Запускаете докер: ***$ docker run --rm -it -v $(pwd):/app phyge***    
- Переходите в папку с проектом внутри Docker'a: ***$ cd app***    
- Запускате сервер: ***$ python PhydgeServer.py***    

*Версии модулей:* 
Для ручной установки.
Python 3.6.4, смотрим **requirenments.txt**
Readability-lxml нужно устанавливать из источников с **https://github.com/buriy/python-readability**
