FROM python:3.6

RUN pip install pipenv

COPY Pipfile* /
RUN pipenv install --system

COPY . /

EXPOSE 8000

CMD ["./bootstrap.sh"]
