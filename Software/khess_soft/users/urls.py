"""
Ce fichier gère spécifiquement les adresses web (URLs) de l'application 'users'.
Il relie une URL tapée dans le navigateur à une fonction (vue) dans views.py.
"""
from django.urls import path
from . import views # Importe toutes les fonctions du fichier views.py


urlpatterns = [
    path('',                views.user_dashboard,     name='user_dashboard'),
    path('cash_register/',  views.cash_register_page, name='cash_register_page'),
    path('update_balance/', views.update_balance,     name='update_balance'),
    path('send-command/',   views.send_command_view,  name='send_command'),
    path('presentation/',   views.presentation,       name='presentation'),

    # Panier session
    path('cart/add/',                    views.add_to_cart,       name='add_to_cart'),
    path('cart/remove/<int:article_id>/',views.remove_from_cart,  name='remove_from_cart'),
    path('cart/clear/',                  views.clear_cart,        name='clear_cart'),

    # NFC
    path('nfc/pay/',      views.nfc_payment_page,    name='nfc_payment_page'),
    path('nfc/confirm/',  views.nfc_confirm_payment, name='nfc_confirm_payment'),
    path('nfc/register/', views.nfc_register_view,   name='nfc_register'),
]


'''
urlpatterns = [
    # L'adresse vide ('') correspond à l'accueil du site. Elle charge le dashboard.
    path('', views.user_dashboard, name="user_dashboard"),
    
    # L'adresse '/cash_register/' charge la page de la caisse enregistreuse.
    path('cash_register/', views.cash_register_page, name="cash_register_page"),
    
    # Cette adresse n'affiche pas de page, elle exécute l'action de mettre à jour le solde.
    path('update_balance/', views.update_balance, name='update_balance'),
    
    # Cette adresse est appelée en arrière-plan (AJAX/Fetch) pour envoyer l'ordre au Bluetooth.
    path('send-command/', views.send_command_view, name='send_command'),
    
    # Page de présentation simple
    path('presentation/', views.presentation, name='presentation'),
]
'''