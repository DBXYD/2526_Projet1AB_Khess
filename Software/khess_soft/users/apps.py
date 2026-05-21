"""
Ce fichier configure le comportement de l'application 'users' au démarrage de Django.
Le chargement des signaux se fait ici pour que Django les prenne en compte au démarrage.
"""
from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        # Lorsque Django a fini de charger, on lui demande d'importer nos signaux
        # pour qu'il commence à "écouter" les événements (création d'utilisateurs, etc).
        #import users.signals
        from . import signals
