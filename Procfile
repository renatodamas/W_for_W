// Configurações do Servidor Heroku
worker: python -m pip install django-heroku
release: python manage.py migrate --noinput
web: gunicorn wfm.wsgi --log-file -
