// Configurações do Servidor Heroku
release:
    python manage.py makemigrations
    python manage.py migrate
web: gunicorn wfm.wsgi --log-file -

