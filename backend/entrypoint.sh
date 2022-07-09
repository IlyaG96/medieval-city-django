#!/bin/sh

/bin/sh -c 'sleep 3'
python manage.py migrate
python manage.py collectstatic --no-input --clear


exec "$@"