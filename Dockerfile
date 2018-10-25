FROM python:3.6.1

RUN set -ex

RUN pip install -U pip pipenv

RUN mkdir /app

COPY app/Pipfile /app/Pipfile
COPY app/Pipfile.lock /app/Pipfile.lock

WORKDIR /app

RUN cat Pipfile && cat Pipfile.lock
RUN pipenv install --verbose

CMD ["/bin/bash"]

EXPOSE 5050
