"""
Fichier de configuration principal du projet Django.
C'est ici que l'on définit la base de données, les applications installées,
la sécurité et les paramètres d'authentification (comme le CAS de l'ENSEA).
"""
from pathlib import Path

# Construit le chemin absolu vers la racine du projet (le dossier qui contient manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# Clé secrète utilisée par Django pour sécuriser les sessions et les mots de passe.
# ATTENTION : Ne jamais partager cette clé en production (sur un vrai serveur) !
SECRET_KEY = 'django-insecure-yika2hedhf3!louf2&djc^%t+9n(kl^pf3qwsnfvfe2dfoku5i'

# Mode débogage. Si True, affiche les pages d'erreur jaunes détaillées de Django.
# ATTENTION : Doit absolument être False en production pour ne pas fuiter de code source.
DEBUG = True

# Liste des noms de domaine autorisés à héberger ce site (ex: ['mon-site.com', '127.0.0.1'])
# L'étoile '*' autorise tout le monde (utile en développement).
ALLOWED_HOSTS = ['*']

# Liste des applications qui composent ce projet.
INSTALLED_APPS = [
    
    # Applications natives de Django (Admin, Authentification, Sessions...)
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Applications tierces (installées via pip)
    'django_cas_ng',  # Gère la connexion avec le portail de l'école (CAS)
    
    # Nos propres applications créées pour ce projet
    'users', 
]

# Les Middlewares filtrent les requêtes entrantes et sortantes.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', # Gère les utilisateurs connectés
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware', # Protège contre les attaques de formulaires
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_cas_ng.middleware.CASMiddleware', # Intercepte les requêtes pour gérer le SSO CAS
]

# Indique le fichier qui sert de "routeur" principal pour les URLs.
ROOT_URLCONF = 'config.urls'

# Configuration du moteur de rendu HTML (les Templates)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [], # Dossiers supplémentaires où chercher des templates HTML
        'APP_DIRS': True, # Dit à Django de chercher dans les dossiers 'templates' de chaque app
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Fichier utilisé pour lancer l'application sur un serveur web traditionnel
WSGI_APPLICATION = 'config.wsgi.application'

# Configuration de la base de données.
# Par défaut, on utilise SQLite qui stocke tout dans un seul fichier 'db.sqlite3'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
 {
 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
 },
 {
 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
 },
 {
 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
 },
 {
 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
 },
]

# --- PARAMÈTRES D'AUTHENTIFICATION CAS (ENSEA) ---
CAS_SERVER_URL = 'https://identites.ensea.fr/cas/' # L'adresse du serveur de l'école
CAS_REDIRECT_URL = '/' # Où renvoyer l'utilisateur après une connexion réussie ?
CAS_LOGOUT_COMPLETELY = True # Déconnecte l'utilisateur de l'application ET du CAS
CAS_LOGOUT_REQUEST_ALLOWED = ('http://127.0.0.1:8000/',)

# On dit à Django d'utiliser le CAS en priorité pour connecter les gens, 
# puis la base de données normale en secours (ModelBackend).
AUTHENTICATION_BACKENDS = (
    'django_cas_ng.backends.CASBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Langue et fuseau horaire du site
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'fr-fr' # Le site parlera français par défaut
TIME_ZONE = 'Europe/Paris' # Heure de Paris
USE_I18N = True
USE_TZ = True

# Configuration des fichiers statiques (CSS, Images, JavaScript)4
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "users" / "static", # Dit à Django où trouver nos images et styles
]

# Type d'identifiant (ID) par défaut pour les nouvelles tables en base de données
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'