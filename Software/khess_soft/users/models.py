"""
Les modèles représentent les tables de la base de données.
Django traduit ces classes en SQL et garde la structure du site cohérente.
"""
from django.contrib.auth.models import User
from django.db import models


class users_custom(models.Model):
    """
    Profil métier rattaché à l'utilisateur Django.
    On y stocke le rôle, le statut, le solde et quelques informations utiles.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, default='No Defined')
    last_name = models.CharField(max_length=255, default='No Defined')
    sold = models.FloatField(default=0)
    class_name = models.CharField(max_length=255, default='No Defined')
    nb_transaction = models.IntegerField(default=0)
    nfc_uid = models.CharField(max_length=50,blank=True,null=True,unique=True,verbose_name="UID carte NFC",)

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
        return f"{self.user.username} ({self.first_name} {self.last_name})"


class Article(models.Model):
    """
    Produit vendable à la KFET.
    Le prix dépend du statut de l'utilisateur.
    """
    name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=0)

    TYPE_CHOICES = [
        ('le_midi', 'Le Midi'),
        ('boisson', 'Boisson'),
        ('snack', 'Snack'),
        ('viennoiseries', 'Viennoiseries'),
    ]

    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='snack')
    price_cotisant = models.FloatField(default=0)
    price_non_cotisant = models.FloatField(default=0)

    def __str__(self):
        return self.name


class Menu(models.Model):
    """
    Menu composite. Son prix est recalculé automatiquement via les signaux.
    """
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0)

    def __str__(self):
        return self.name


class MenuDetails(models.Model):
    """
    Table de liaison entre un menu et ses articles.
    """
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.menu.name} - {self.article.name}"


class Transaction(models.Model):
    """
    En-tête d'une transaction.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.price} €"


class TransactionDetails(models.Model):
    """
    Détail ligne par ligne d'une transaction.
    """
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

    def __str__(self):
        return f"{self.user.username} - {self.article.name} x{self.quantity}"


class Cash(models.Model):
    """
    Vue comptable globale de la caisse.
    """
    sold_cash = models.FloatField()
    gain_card = models.FloatField()
    gain_cash = models.FloatField()
    total = models.FloatField()

    def __str__(self):
        return f"Total caisse: {self.total} €"


'''
"""
Les Modèles (Models) sont la représentation Python des tables de la base de données.
Django va traduire ce code en requêtes SQL automatiquement.
"""
from django.contrib.auth.models import User
from django.db import models

class UserCustom(models.Model):
    """
    Ce modèle étend l'utilisateur de base de Django (User).
    Il ajoute des champs spécifiques à notre projet comme le solde, le rôle et le statut.
    On utilise OneToOneField car un User de Django ne peut avoir qu'un seul UserCustom.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Si l'User est supprimé, le profil est supprimé avec.
    first_name = models.CharField(max_length=255, default='Non défini')
    last_name = models.CharField(max_length=255, default='Non défini')
    sold = models.FloatField(default=0.0) # Solde de l'utilisateur (argent sur sa carte)
    class_name = models.CharField(max_length=255, default='Inconnu') # Classe de l'élève (ex: 1A, 2A)
    nb_transaction = models.IntegerField(default=0)

    # Choix restreints pour les menus déroulants dans l'administration
    ROLE_CHOICES = [
        ('admin', 'Admin'), 
        ('respo', 'Responsable'), 
        ('student', 'Étudiant')
        ]
    STATUS_CHOICES = [
        ('cotisant', 'Cotisant'), 
        ('non_cotisant', 'Non Cotisant'), 
        ('prof', 'Professeur')
        ]
    
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='student')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='non_cotisant')
    created_at = models.DateTimeField(auto_now_add=True) # Enregistre l'heure de création automatiquement



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


    def __str__(self):
        # Définit comment l'objet s'affiche dans le panneau d'administration (ex: "jean.dupont (Jean)")
        return f"{self.user.username} ({self.first_name})"

class Article(models.Model):
    """ Représente un produit vendable à la KFET (un coca, un snickers...) """
    name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=0) # Stock disponible
    TYPE_CHOICES = [('sandwich', 'Sandwich'), ('boisson', 'Boisson'), ('snack', 'Snack')]
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='snack')
    price = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

class Menu(models.Model):
    """ Représente un groupement d'articles (ex: Menu Étudiant) """
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.0) # Ce prix sera mis à jour automatiquement par les signaux

    def __str__(self):
        return self.name

class MenuDetails(models.Model):
    """
    Table de liaison entre un Menu et un Article.
    C'est ce qu'on appelle une relation "Many-to-Many" détaillée.
    Un menu peut avoir plusieurs articles, et un article peut être dans plusieurs menus.
    """
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

class Transaction(models.Model):
    """ Représente un historique d'achat ou de recharge de solde. """
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Quel utilisateur a fait la transaction ?
    price = models.FloatField() # Montant (positif pour une recharge, négatif pour un achat)
    created_at = models.DateTimeField(auto_now_add=True)

'''