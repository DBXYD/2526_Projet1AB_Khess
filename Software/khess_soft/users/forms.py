"""
Formulaires simples pour éditer les données métier.
Ces formulaires sont pratiques pour des vues d'administration ou des écrans de gestion.
"""
from django import forms
from .models import users_custom, Article


class UsersCustomForm(forms.ModelForm):
    class Meta:
        model = users_custom
        fields = ['first_name', 'last_name', 'class_name', 'sold', 'role', 'status']


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['name', 'quantity', 'type', 'price_cotisant', 'price_non_cotisant']