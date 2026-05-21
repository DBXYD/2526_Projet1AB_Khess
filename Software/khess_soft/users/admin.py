"""
Configuration de l'interface d'administration Django.
Les gérants peuvent gérer les utilisateurs, produits, menus et transactions ici.
"""
from django.contrib import admin
from .models import users_custom, Article, Menu, MenuDetails, Transaction, TransactionDetails, Cash


@admin.register(users_custom)
class UsersCustomAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'role', 'status', 'sold', 'nb_transaction', 'created_at')
    search_fields = ('user__username', 'first_name', 'last_name')
    list_filter = ('role', 'status', 'class_name')


class MenuDetailsInline(admin.TabularInline):
    """
    Permet d'ajouter les articles d'un menu directement dans la fiche Menu.
    """
    model = MenuDetails
    extra = 1


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    inlines = [MenuDetailsInline]
    list_display = ('name', 'price')
    search_fields = ('name',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'type', 'price_cotisant', 'price_non_cotisant')
    list_filter = ('type',)
    search_fields = ('name',)


@admin.register(MenuDetails)
class MenuDetailsAdmin(admin.ModelAdmin):
    list_display = ('menu', 'article')
    search_fields = ('menu__name', 'article__name')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'price', 'created_at')
    search_fields = ('user__username',)
    list_filter = ('created_at',)


@admin.register(TransactionDetails)
class TransactionDetailsAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'user', 'article', 'quantity', 'price', 'payment_type', 'created_at')
    search_fields = ('user__username', 'article__name')
    list_filter = ('payment_type', 'type', 'created_at')


@admin.register(Cash)
class CashAdmin(admin.ModelAdmin):
    list_display = ('sold_cash', 'gain_card', 'gain_cash', 'total')
'''
"""
Ce fichier configure l'apparence de la page /admin/ du site.
Il permet aux gérants de la KFET d'ajouter facilement des produits sans coder.
"""
from django.contrib import admin
from .models import UserCustom, Article, Menu, MenuDetails, Transaction, TransactionDetails

@admin.register(UserCustom)
class UserCustomAdmin(admin.ModelAdmin):
    # Colonnes affichées dans la liste des utilisateurs
    list_display = ('user', 'role', 'status', 'sold', 'created_at')

class MenuDetailsInline(admin.TabularInline):
    """
    Permet d'ajouter des articles directement DEPUIS la page de création d'un menu.
    C'est beaucoup plus pratique que de devoir créer les liens un par un.
    """
    model = MenuDetails
    extra = 2 # Affiche 2 lignes vides par défaut pour ajouter des articles rapidement

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    inlines = [MenuDetailsInline] # Intègre le bloc ci-dessus dans la page Menu
    list_display = ('name', 'price') # Affiche le nom et le prix calculé

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'type', 'price')
    list_filter = ('type',) # Ajoute une barre latérale pour filtrer (seulement boissons, etc.)

# Enregistrement standard pour les autres tables
admin.site.register(MenuDetails)
admin.site.register(Transaction)
admin.site.register(TransactionDetails)

'''