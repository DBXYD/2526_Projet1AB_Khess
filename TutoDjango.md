# 🛒 Projet Caisse Enregistreuse - Tuto Django

> **Projet Ingénieur** : Système de gestion de commandes et de base de données.

Ce projet permet de gérer une caisse enregistreuse via une interface web. Il utilise **Django** pour le backend et une base de données **SQLite**.

---

## 🛠️ Installation et Configuration

Pour faire fonctionner le projet sur votre machine (Linux/Ubuntu), suivez ces étapes dans votre terminal de VS code.

### 1. Préparation de l'environnement virtuel
```bash
# Crée le dossier de l'environnement virtuel nommé 'venv'
python3 -m venv venv

# Active l'environnement (indispensable avant chaque séance de travail)
# Vous devriez voir (venv) apparaître à gauche de votre curseur
source venv/bin/activate
```

### 2. Installation de Django et des modules
Une fois l'environnement activé, installez les bibliothèques Python indispensables :
```bash
# Installe le framework web principal
pip install django

# Installe le module pour l'authentification centralisée de l'école
pip install django-cas-ng
```

### 3. Lancement du serveur de développement
Accédez au dossier contenant le fichier manage.py et lancez le moteur du site :
```bash
# Se déplacer dans le dossier racine du projet
cd DatabaseCashRegister

# Démarre le serveur local
python3 manage.py runserver
```
Le site est maintenant accessible sur votre navigateur à l'adresse : http://127.0.0.1:8000/

### 🧭 Navigation sur le site

Pour accéder aux différentes pages, vous devez ajouter le chemin correspondant à la fin de l'URL `http://127.0.0.1:8000/`. Vous pouvez retrouver ces chemins dans le fichier urls.py sous la variable urlpatterns.

Voici les accès principaux pour ce projet :

| Page | Chemin à ajouter | URL complète |
| :--- | :--- | :--- |
| **Accueil** | `/` | http://127.0.0.1:8000/ |
| **Administration** | `admin/` | http://127.0.0.1:8000/admin/ |
| **Caisse** | `cash_register_page/` | http://127.0.0.1:8000/cash_register_page/ |
| **Présentation** | `présentation/` | http://127.0.0.1:8000/présentation/ |

### 🛠️ Résolution du problème "DoesNotExist" (Page d'accueil vide)

Si l'adresse http://127.0.0.1:8000/admin/ fonctionne mais que la page d'accueil http://127.0.0.1:8000/ affiche une erreur, c'est parce que votre utilisateur n'est pas encore enregistré dans la table users_custom.

Voici comment régler ça :
1. Connectez-vous sur l'interface d'administration : http://127.0.0.1:8000/admin/.
2. Dans la section Users_Custom, cliquez sur Add (Ajouter).
3. Remplissez les informations en veillant à ce que le nom d'utilisateur corresponde exactement à celui avec lequel vous essayez de vous connecter.
4. Enregistrez, puis retournez sur la page d'accueil.

### 🗄️ Visualiser la Base de Données sur VS Code
Pour explorer les tables (produits, ventes, utilisateurs) sans quitter votre éditeur de code :
1. Allez dans l'onglet Extensions de VS Code (icône carrée à gauche).
2. Recherchez et installez les extensions : SQLite et SQLite Viewer.
3. Une fois installées, vous pourrez ouvrir le fichier db.sqlite3 pour voir les données sous forme de tableaux clairs.

### 🔐 Créer ou Modifier un compte Administrateur
Si vous avez une erreur 403 Forbidden ou si votre compte n'a pas les droits, vous pouvez forcer les privilèges "Staff" (Directeur) via la console Python de Django.
1. Entrez dans le mode "Shell" (console interactive)
```bash
python3 manage.py shell
```
2. Copiez et collez ces lignes de code une par une :
```bash
from django.contrib.auth.models import User
u = User.objects.get(username='ton_nom_utilisateur_ensea')
u.is_staff = True
u.is_superuser = True
u.save()
exit()
```
### 🖼️ Changer l'image d'un produit

1. **Nommer l'image** : Renommez votre fichier exactement comme le nom du produit (ex: `coca cola.png`).
2. **Ajouter le fichier** : Déposez-le dans `users/static/users/images/`.
3. **Modifier le code** : Dans votre fichier HTML, remplacez la ligne `<img>` par :
   `<img src="{% static 'users/images/' %}{{ article.name }}.png" alt="{{ article.name }}" class="img-fluid mb-2" style="max-height: 100px;">`
4. **Actualiser** : Sauvegardez (**CTRL+S**) et rafraîchissez le navigateur (**CTRL+F5**).




