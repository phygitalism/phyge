FROM python:3.6.1

RUN set -ex

RUN pip install -U pip pipenv

RUN mkdir -p project/app

COPY Pipfile /project/Pipfile
COPY Pipfile.lock /project/Pipfile.lock

WORKDIR /project

RUN cat Pipfile && cat Pipfile.lock
RUN pipenv install --verbose

CMD ["/bin/bash"]

EXPOSE 5050
