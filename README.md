## PokeTest

C'est un projet utilisant les endpoints de l'API PokeAPI.


## Prérequis

- Cloner le projet
- Avoir virtualenv, se créer un environnement virtuel et installer les packages du fichier requirements.txt à la racine du projet.
- Se déplacer à la racine du projet avec un terminal de commande


## Lancement du serveur

python manage.py runserver


## Postman 

Une collection Postman se situe à la racine du projet et permet de facilement utiliser les endpoints de l'API.
Les identifiants à utiliser ont été insérés en base données avec le script dataset_script.py .
A la première utilisation il faut utiliser l'endpoint login pour récupérer un jeton, et le coller dans le champ Authorization de la collection.
Type : API Key
Key : Authorization 
Value : Token jeton_à_coller


## Lancement des tests

Lancer la commande : python manage.py test

## Logs

Des fichiers de logs sont disponible dans le dossier logs.
