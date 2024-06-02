#!/bin/sh

# Activate the virtual environment
. /py/bin/activate

cd /backend/app
# Wait for the database to be ready
python manage.py wait_for_db

# Run database migrations
python manage.py migrate --no-input

# Collect static files
python manage.py collectstatic --no-input

# Start Gunicorn
exec gunicorn api.wsgi:application --bind 0.0.0.0:8000
