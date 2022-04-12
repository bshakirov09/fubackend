#!/usr/bin/env bash

echo "Collecting static files"
python manage.py collectstatic

echo "Starting the server"
gunicorn --reload -b 0.0.0.0:8001 fitness.wsgi:application --preload --workers 3 --timeout 300 --graceful-timeout 10 --log-level info --log-file -