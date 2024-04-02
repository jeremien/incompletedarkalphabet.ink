# Pour démarrer

`python -m venv venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

`flask run`

`gunicorn --bind 0.0.0.0:5000 wsgi:app`

