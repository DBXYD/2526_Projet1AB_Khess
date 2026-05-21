"""
URL configuration for DatabaseDjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

"""
Ce fichier est le "standardiste" du projet.
Quand un utilisateur tape une adresse web, ce fichier décide quelle application doit répondre.
"""
from django.contrib import admin
from django.urls import path, include
from django_cas_ng import views as cas_views

urlpatterns = [
    # 1. Accès au panneau d'administration (ex: mon-site.com/admin/)
    path('admin/', admin.site.urls),
    
    # 2. Les routes gérées par le module CAS (pour se connecter/déconnecter via l'école)
    path('accounts/login/', cas_views.LoginView.as_view(), name='cas_ng_login'),
    path('accounts/logout/', cas_views.LogoutView.as_view(), name='cas_ng_logout'),
    path('accounts/callback/', cas_views.CallbackView.as_view(), name='cas_ng_proxy_callback'),
    
    # 3. Toutes les autres adresses (la racine du site '') sont envoyées
    # au fichier urls.py de notre application 'users' pour qu'elle s'en occupe.
    path('', include('users.urls')),
]