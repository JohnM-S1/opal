#!/bin/bash

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput

#mod_wsgi-express start-server opal/wsgi.py
mod_wsgi-express start-server --url-alias /static static opal/wsgi.py




