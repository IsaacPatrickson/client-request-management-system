#!/bin/sh
PORT=${PORT:-8000}

echo "Collecting static files..."
python manage.py collectstatic --noinput

if [ "$DJANGO_ENV" = "production" ]; then
    echo "Starting Gunicorn server"
    gunicorn mysite.wsgi:application --bind 0.0.0.0:$PORT
else
    echo "Starting Django development server"
    python manage.py runserver 0.0.0.0:$PORT
fi
