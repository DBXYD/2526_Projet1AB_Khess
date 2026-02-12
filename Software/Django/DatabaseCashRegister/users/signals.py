from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import MenuDetails, Menu

# Create your signals here.
@receiver(post_save, sender=MenuDetails)
@receiver(post_delete, sender=MenuDetails)
def update_menu_price(sender, instance, **kwargs):
    menu = instance.menu
    
    total_price=sum(detail.article.price for detail in menu.menudetails_set.all())
    menu.price = total_price
    menu.save()