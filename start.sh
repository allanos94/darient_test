python3.9 manage.py makemigrations --noinput
python3.9 manage.py migrate --noinput

gunicorn investment_manager.wsgi:application --bind 0.0.0.0:$PORT