#!/bin/bash

#service nginx start
python3 manage.py collectstatic --noinput
#python3 manage.py task_runner &
python3 manage.py migrate
ln -s staticfiles static
python3 -m http.server 9000 &
#gunicorn --config gunicorn-cfg.py piekarniaApi.wsgi // uncomment for prod
python3 manage.py runserver 0.0.0.0:8000