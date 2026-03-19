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

1. **Nommer l'image** : Renommez votre fichier image exactement comme le nom du produit dans l'interface Administration (ex: `coca cola.png`). Attention aux espaces et aux minuscules !
2. **Ajouter le fichier** : Déposez votre image dans le dossier VS Code suivant : `users/static/users/images/`
3. **Modifier le code** : Dans votre fichier HTML `cash_register.html`, remplacez les lignes `<img>` par :
   `<img src="{% static 'users/images/' %}{{ article.name }}.png" alt="{{ article.name }}" class="img-fluid mb-2" style="max-height: 100px;">`
4. **Actualiser** : Enregistrez votre fichier (**CTRL + S**) puis rafraîchissez le navigateur avec **CTRL + F5** pour forcer le chargement des nouvelles images.

Si vos images sont au format .jpg, remplacez simplement .png par .jpg à la fin de la ligne de code ci-dessus. Toutes vos photos devront alors avoir le même format.

### 📂 Ajouter une nouvelle catégorie de produits

Pour ajouter un nouvel onglet (ex: Viennoiseries) et afficher les produits correspondants, il faut suivre ces étapes suivantes :

1. Modifier le Modèle (models.py)
 Ajoutez la catégorie dans la base de données.

```bash
TYPE_CHOICES = [
    ('sandwich', 'Sandwich'),
    ('boisson', 'Boisson'),
    ('snack', 'Snack'),
    ('viennoiseries', 'Viennoiseries'), # <-- Nouvelle ligne
]
```

2. Mettre à jour la Vue (views.py)
Mise à jour de la liste pour le menu latéral.
```bash
def cash_register_page(request):
    articles = Article.objects.all()
    categories = ['Tout', 'Menu', 'Sandwich', 'Snack', 'Boisson', 'Viennoiseries'] 
    return render(request, 'users/cash_register.html', {
        'article_items': articles, 
        'categories': categories
    })
]
```
3.Créer la section dans le HTML (cash_register.html)
Copie ce bloc à la suite des autres : 
```bash
<div id="viennoiseries" class="category-section">
    <h2 class="mt-4">Viennoiseries</h2>
    <div class="row">
        {% for article in article_items %}
            {% if article.type == 'viennoiseries' %}
                <div class="col-md-2 mb-4">
                    <button class="btn btn-light w-100 shadow-sm rounded" style="height: 200px;">
                        <div class="d-flex flex-column align-items-center">
                            <img src="{% static 'users/images/' %}{{ article.name }}.png" class="img-fluid mb-2" style="max-height: 100px;">
                            <span class="fw-bold">{{ article.name }}</span>
                            <span class="text-muted">{{ article.price }} €</span>
                        </div>
                    </button>
                </div>
            {% endif %}
        {% endfor %}
    </div>
</div>
```
Sauvegardez (CTRL+S) et redémarrez le serveur.

### 💳 Implémenter une double tarification (Cotisant vs Non-Cotisant)

1. models.py (La Base)
C'est ici que l'on définit les deux colonnes de prix.
```bash
class Article(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=0)
    TYPE_CHOICES = [('le midi', 'Le Midi'), ('boisson', 'Boisson'), ('snack', 'Snack'),('viennoiseries', 'Viennoiseries')]
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='snack')
    # Les deux nouveaux champs de prix
    price_cotisant = models.FloatField(default=0)
    price_non_cotisant = models.FloatField(default=0)
```
2. admin.py (L'interface de gestion)
```bash
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'type', 'price_cotisant', 'price_non_cotisant')
    list_filter = ('type',)
```

3. views.py (La Logique de sélection)

```bash
## Récupération des articles :
    article_items = []
    for article in article_data:
        # Condition pour choisir le prix
        if user_data.status == 'Cotisant':
            prix_final = article.price_cotisant
        else:
            prix_final = article.price_non_cotisant
            
        article_items.append({
            'name': article.name, 
            'quantity': article.quantity, 
            'type': article.type, 
            'price': prix_final
        })
```

4. Les commandes Terminal (Indispensables)
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
### 🖥️ Afficher deux tarifs (C & NC) sur l'interface Web 

1. Dans views.py
On change juste ce qu'on envoie dans le dictionnaire pour inclure les deux variables.
```bash
article_items.append({
      'name': article.name,
      'type': article.type,
      'price_c': article.price_cotisant,     
      'price_nc': article.price_non_cotisant
```

2. Dans cash_register.html
```bash
<span class="text-muted" style="font-size: 0.8em;">Cotisant : {{ article.price_c }} €</span>
<span class="text-muted" style="font-size: 0.8em;">Non Cotisant : {{ article.price_nc }} €</span>
```

   













