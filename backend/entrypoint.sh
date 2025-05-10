#!/bin/sh

python manage.py makemigrations
python manage.py migrate
python -m gunicorn --bind 0.0.0.0:8000 --workers 3 backend.wsgi:application