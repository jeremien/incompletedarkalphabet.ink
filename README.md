
# Pour démarrer

`python -m venv venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

`python -m flask --app incomplete run --port 8000 --debug`

`gunicorn --bind 0.0.0.0:5000 incomplete:create_app`

`gunicorn --bind 0.0.0.0:5000 'incomplete:create_app()'`

`ps aux|grep gunicorn`

kill -9 pid

dev
install package npm
