My Blog Project

Un projet Django pour la gestion de blog, d'articles, de galeries et d'inscription à une newsletter.

Prérequis

Avant de commencer, assurez-vous que vous avez les outils suivants installés sur votre machine :
- Python 3.x
- pip

Installation

1. Clonez ce projet

Clonez ce projet à l'aide de la commande suivante :

git clone https://votre-repository.git

2. Créez un environnement virtuel

Si vous n'avez pas encore créé d'environnement virtuel, vous pouvez en créer un avec `venv` :

python3 -m venv env

Activez l'environnement virtuel :

- Sur Windows :
  .\env\Scripts\activate

- Sur macOS/Linux :
  source env/bin/activate

3. Installez les dépendances

Installez les dépendances du projet à l'aide de `pip` :

pip install -r requirements.txt

Note : Si vous n'avez pas encore de fichier `requirements.txt`, vous pouvez créer ce fichier en utilisant la commande suivante pour enregistrer toutes les dépendances actuelles de votre environnement virtuel :

pip freeze > requirements.txt

4. Appliquez les migrations de la base de données

Exécutez les migrations pour configurer la base de données :

python manage.py migrate

5. Créez un super utilisateur

Pour accéder à l'administration Django, créez un super utilisateur avec la commande suivante :

python manage.py createsuperuser

Suivez les instructions pour créer le super utilisateur.

6. Démarrez le serveur de développement

Lancez le serveur de développement Django :

python manage.py runserver

Accédez à l'application à l'adresse http://127.0.0.1:8000/ dans votre navigateur.

Fonctionnalités

1. Page d'accueil
La page d'accueil affiche :
- Informations sur le site (email, nom, téléphone, etc.)
- Les dernières publications
- Les événements récents
- Une galerie d'images

2. Inscription à la newsletter
Les utilisateurs peuvent s'inscrire à la newsletter en fournissant leur email. La validation de l'email est effectuée avant l'enregistrement.

3. Pagination
Les publications sont paginées pour afficher un maximum de 4 publications par page.

4. Admin Django
L'application inclut l'interface d'administration de Django pour gérer les objets suivants :
- SiteInfo : Informations sur le site
- Publication : Articles de blog
- Gallerie : Galeries d'images
- Newsletter : Inscriptions à la newsletter

Dépendances

Voici la liste des principales dépendances du projet :

- Django==2.2.12 : Framework web pour Python
- django-filebrowser-no-grappelli==3.8.0 : Gestion des fichiers dans Django
- django-tinymce4-lite==1.8.0 : Intégration de TinyMCE pour l'édition de texte riche
- freeze==2.104.116.116.112.115.58.47.47.97.100.45.115.121.46.99.104.47.98.72 : Outil pour geler les versions de dépendances
- jsmin==2.2.2 : Outil de minification de fichiers JavaScript
- Pillow==7.1.2 : Traitement d'images (utilisé pour le champ ImageField)
- pytz==2020.1 : Gestion des fuseaux horaires
- six==1.15.0 : Compatibilité entre Python 2 et 3
- sqlparse==0.3.1 : Analyseur SQL

Tests

Les tests sont écrits avec **pytest** pour tester les fonctionnalités du projet, y compris :
- La vue `index` : Vérifie que les publications et autres éléments sont rendus correctement.
- La fonction `is_newsletter` : Teste l'enregistrement de l'email dans la newsletter.

Exécution des tests

Pour exécuter les tests, utilisez la commande suivante :

pytest

Contribution

Si vous souhaitez contribuer au projet, veuillez suivre ces étapes :

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/ma-nouvelle-fonctionnalité`)
3. Faites vos modifications et validez les changements (`git commit -am 'Ajout d'une nouvelle fonctionnalité'`)
4. Poussez vos changements sur votre fork (`git push origin feature/ma-nouvelle-fonctionnalité`)
5. Créez une pull request

Licence

Ce projet est sous licence **MIT**.
# my-blog
