# MLX


### Run (with Docker)

Bringing all containers up with:

```sh
$ cd phyge
$ ./run.sh
``` 
This script will install development environment and start services.

### Training model

Just run:

```sh
$ ./train.sh
```

It will seed database and train both model LSI and LDA.
### Dropping database volume

If you need to reimport data, run:

```sh
$ ./drop_db.sh
```

### Installation (with venv)
**IN PROGRESS**

*Версии модулей:* 
Для ручной установки.
Python 3.6.4, смотрим **requirenments.txt**
Readability-lxml нужно устанавливать из источников с **https://github.com/buriy/python-readability**
