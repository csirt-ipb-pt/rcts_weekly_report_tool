#!/bin/sh

set -e

python3 manage.py collectstatic --noinput

python3 manage.py makemigrations

python3 manage.py migrate 

uwsgi --socket :8000 --master --enable-threads --modul weekly_reports.wsgi