"""
Signaux Django.
Ils permettent de synchroniser automatiquement les données métier avec la base.
"""
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Article, Menu, MenuDetails, Transaction, TransactionDetails, users_custom


def recalculate_menu_price(menu):
    """
    Recalcule le prix d'un menu à partir des prix cotisant de ses articles.
    """
    total = MenuDetails.objects.filter(menu=menu).aggregate(
        total=Sum('article__price_cotisant')
    )['total'] or 0

    menu.price = total
    menu.save(update_fields=['price'])


def recalculate_menus_for_article(article):
    """
    Recalcule tous les menus qui contiennent un article modifié.
    """
    menus = Menu.objects.filter(menudetails__article=article).distinct()
    for menu in menus:
        recalculate_menu_price(menu)


def adjust_article_stock(article_id, delta):
    """
    Ajoute ou retire une quantité au stock d'un article.
    delta négatif = sortie de stock.
    delta positif = retour de stock.
    """
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        return

    article.quantity = max(0, article.quantity + delta)
    article.save(update_fields=['quantity'])


@receiver([post_save, post_delete], sender=MenuDetails)
def update_menu_price(sender, instance, **kwargs):
    recalculate_menu_price(instance.menu)


@receiver([post_save, post_delete], sender=Article)
def update_related_menus_when_article_changes(sender, instance, **kwargs):
    recalculate_menus_for_article(instance)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Crée automatiquement le profil métier quand un User Django est créé.
    """
    if created:
        users_custom.objects.create(
            user=instance,
            first_name=instance.first_name or "No Defined",
            last_name=instance.last_name or "No Defined",
        )


@receiver(post_save, sender=Transaction)
def increment_transaction_count(sender, instance, created, **kwargs):
    """
    Compte les transactions de l'utilisateur.
    """
    if not created:
        return

    profile, _ = users_custom.objects.get_or_create(user=instance.user)
    profile.nb_transaction += 1
    profile.save(update_fields=['nb_transaction'])


@receiver(post_delete, sender=Transaction)
def decrement_transaction_count(sender, instance, **kwargs):
    """
    Décrémente le compteur si une transaction est supprimée.
    """
    try:
        profile = users_custom.objects.get(user=instance.user)
    except users_custom.DoesNotExist:
        return

    if profile.nb_transaction > 0:
        profile.nb_transaction -= 1
        profile.save(update_fields=['nb_transaction'])


@receiver(post_save, sender=TransactionDetails)
def decrease_stock_on_new_transaction_detail(sender, instance, created, **kwargs):
    """
    Lorsqu'une ligne de vente est créée, on décrémente le stock.
    """
    if created:
        adjust_article_stock(instance.article_id, -instance.quantity)


@receiver(post_delete, sender=TransactionDetails)
def restore_stock_on_transaction_detail_delete(sender, instance, **kwargs):
    """
    Lorsqu'une ligne de vente est supprimée, on remet le stock.
    """
    adjust_article_stock(instance.article_id, instance.quantity)
'''
"""
Les signaux permettent d'exécuter du code automatiquement quand un événement survient
dans la base de données (comme une sauvegarde ou une suppression).
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from django.contrib.auth.models import User
from .models import MenuDetails, UserCustom

@receiver([post_save, post_delete], sender=MenuDetails)
def update_menu_price(sender, instance, **kwargs):
    """
    Quand on ajoute ou on retire un article d'un menu (MenuDetails),
    cette fonction recalcule automatiquement le prix total du menu concerné.
    """
    menu = instance.menu
    # On demande à la base de données d'additionner (Sum) les prix de tous les articles de ce menu.
    result = menu.menudetails_set.aggregate(total=Sum('article__price'))
    #total_price=sum(detail.article.price for detail in menu.menudetails_set.all())

    menu.price = result['total'] or 0.0 # Si c'est vide, le prix est 0.0
    #menu.price = total_price
    menu.save() # On sauvegarde le nouveau prix du menu

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Très important pour le CAS ! 
    Dès qu'un nouvel "User" se connecte pour la première fois via le système de l'école,
    ce signal lui crée automatiquement son "UserCustom" (son profil avec le solde à 0).
    """
    if created:
        UserCustom.objects.create(
            user=instance,
            first_name=instance.first_name or "Nouvel",
            last_name=instance.last_name or "Utilisateur"
        )

'''