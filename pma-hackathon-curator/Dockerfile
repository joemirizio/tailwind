FROM python:3.6

RUN pip install pipenv

COPY Pipfile* /
RUN pipenv install --system

COPY * /

RUN python manage.py migrate
RUN python manage.py loaddata $(ls curator/fixtures)
RUN python manage.py loadmodels

EXPOSE 8000

CMD ["python", "manage.py", "runserver"]