from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class users_custom(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, default='No Defined')
    last_name = models.CharField(max_length=255, default='No Defined')
    sold = models.FloatField(default=0)
    class_name = models.CharField(max_length=255, default='No Defined')
    nb_transaction = models.IntegerField(default=0)
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('respo', 'Responsable'),
        ('student', 'Étudiant'),
    ]
    STATUS_CHOICES = [
        ('cotisant', 'Cotisant'),
        ('non_cotisant', 'Non Cotisant'),
        ('prof', 'Professeur'),
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='student')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='non_cotisant')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Article(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=0)
    TYPE_CHOICES = [('sandwich', 'Sandwich'), ('boisson', 'Boisson'), ('snack', 'Snack')]
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='snack')
    price = models.FloatField(default=0)


class Menu(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0)


class MenuDetails(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.menu.name} - {self.article.name}"


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.price} €"

class TransactionDetails(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    quantity = models.IntegerField()
    price = models.FloatField()
    payment_type = models.CharField(max_length=50, choices=[
        ('cash', 'Cash'),
        ('card', 'Card'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)

class Cash(models.Model):
    sold_cash = models.FloatField()
    gain_card = models.FloatField()
    gain_cash = models.FloatField()
    total = models.FloatField()