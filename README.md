# Développement

## Cloner le dépôt
`git clone https://github.com/jeremien/incompletedarkalphabet.ink.git`

## Configuration

- fichier `config.yml`

## Structure de l'application

- dossier avec les images d'origine
`../src/`

- dossier avec les images de destination
`../incomplete/static/assets/images/`


## Pour démarrer

- Création d'un environnement python
`python -m venv venv`

- Activation
`source venv/bin/activate`

- Installation des dépendances
`pip install -r requirements.txt`

- Serveur de développement
`flask run`

- Serveur de production
`gunicorn --bind 0.0.0.0:5000 wsgi:app`

## CLI

- commande pour convertir les images dans *src*
`flask process`

# Libraries

- [Flask](https://flask.palletsprojects.com/en/3.0.x/)
- [Lazysizes.js](https://github.com/aFarkas/lazysizes)
- [Paged.js](https://gitlab.coko.foundation/pagedjs/)
