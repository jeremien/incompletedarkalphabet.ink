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

- commande pour convertir les images dans *src* vers *assets/images*
`flask process`

- commande pour supprimer les images dans *assets/images*
`flask clean`

## TODO

- config : ajouter partie livre css format/marge
- config : configuration du traitement des images
- config : choisir les chemins d'entrée/sortie
- image : ajouter fonctionnalité pour contraste
- image : fonctionnalité détourage
- bug: choix du format jpg ne fonctionne pas
