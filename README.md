# Projet de semestre Crust Break

## Lancement et setup du projet
- Cloner le projet en local ou un/le serveur : `git clone https://github.com/BaptisteZloch/Crust-Break-backend.git`
- Créer l'environnement virtuel : `python -m venv venv`
- Activer l'environnement virtuel :
  - Sous Linux & MacOS : `source venv/bin/activate`
  - Sous Windows : `.\venv\Scripts\activate`
- Installer les dépendances : `pip install -r requirements.txt`
- Une fois la base de données prête il faut executer les migrations permettant de créer les tables de l'application et du projet pour cela executez les commandes suivantes dans la cmd/powershell, bash :
  
    `python manage.py makemigrations`

    `python manage.py migrate`

    `python manage.py makemigrations crust_break_recette_api`

    `python manage.py migrate crust_break_recette_api`

- A présent la base de données est remplie avec les tables mais elle ne contient aucune données.
- Pour lancer le serveur django : `python manage.py runserver` pour le run sur une autre adresse IP ou un autre port : `python manage.py runserver 0.0.0.0:8070`