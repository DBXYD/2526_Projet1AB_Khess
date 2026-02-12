from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import  users_custom, Article, Menu, MenuDetails, Transaction, TransactionDetails
# Register your models here.
@admin.register(users_custom)
class UserCustomAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'status', 'sold', 'created_at')

class MenuDetailsInline(admin.TabularInline):
    model = MenuDetails
    extra = 2  # Nombre de lignes vides par défaut pour ajouter des articles

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    inlines = [MenuDetailsInline]  # Ajoute les articles associés directement dans le menu
    list_display = ('name', 'price')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'type', 'price')
    list_filter = ('type',)

admin.site.register(MenuDetails)
admin.site.register(Transaction)
admin.site.register(TransactionDetails)