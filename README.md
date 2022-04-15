# Projet de semestre Crust Break

## Lancement et setup du projet
### Initialisation :
- Cloner le projet en local ou un/le serveur : `git clone https://github.com/BaptisteZloch/Crust-Break-backend.git`
### Dépendances :
- Créer l'environnement virtuel : `python -m venv venv`
- Activer l'environnement virtuel :
  - Sous Linux & MacOS : `source venv/bin/activate`
  - Sous Windows : `.\venv\Scripts\activate`
- Installer les dépendances : `pip install -r requirements.txt`
### Base de données :
- Ensuite il faut créer une base de données sous MySQL : 
```sql
CREATE DATABASE <the_name_you_want>
```
- Puis modifier les identifiants et le nom de la base de données dans le fichier `settings.py` :
```py
DATABASES = {
   'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': '<the_name_you_want>',
        'USER': 'newuser',
        'PASSWORD': 'crn-bdd2603',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}
```
- Une fois la base de données prête il faut executer les migrations permettant de créer les tables de l'application et du projet pour cela executez les commandes suivantes dans la cmd/powershell, bash :
  
    `python3 manage.py makemigrations`

    `python3 manage.py migrate`

    `python3 manage.py makemigrations crust_break_user_api`

    `python3 manage.py migrate crust_break_user_api`

- A présent la base de données est remplie avec les tables mais elle ne contient aucune données.
### Lancement du serveur :
- Pour lancer le serveur django : `python manage.py runserver` pour le run sur une autre adresse IP ou un autre port : `python manage.py runserver 0.0.0.0:8070`