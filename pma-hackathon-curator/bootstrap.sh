#!/bin/bash

python manage.py migrate
python manage.py loadmodels ${API_URI}
python manage.py loaddata $(ls curator/fixtures/*.json)
python manage.py loadfacts curator/fixtures/manual/artwork_facts.json

python manage.py runserver 0.0.0.0:8000
