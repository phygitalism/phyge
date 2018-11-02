# PHYGE
<p align="center"> <img src="./icon.jpg" width="250"> </p>

### Run (with Docker)

Bringing all containers up with:

```sh
$ cd phyge
$ ./run.sh
```
This script will install development environment and start services (with pipevn). // may take considerable time

### Training model

Just run:

```sh
$ ./train.sh
```

It will seed database and train both model LSI.
### Dropping database volume

If you need to reimport data, run:

```sh
$ ./drop_db.sh
```

Read more in [Description.md](./app/Description.md)
