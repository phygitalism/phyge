FROM python:3.6.1

RUN set -ex

RUN pip install -U pip pipenv

RUN mkdir -p project/app

COPY Pipfile /project/Pipfile

WORKDIR /project

RUN pipenv install

CMD ["/bin/bash"]

EXPOSE 5050