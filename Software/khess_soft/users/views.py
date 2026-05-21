"""
Vues principales de l'application users.
Elles gèrent la caisse, le tableau de bord, les soldes et la communication Bluetooth.
"""
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from django.db import transaction as db_transaction
from .Module_NFC import read_nfc_uid_once

NFC_SERIAL_PORT = '/dev/ttyUSB0'  # Adaptez selon votre machine

from .Module_Communication import send_bluetooth_command
from .models import Article, Menu, Transaction, TransactionDetails, users_custom


def presentation(request):
    """
    Page publique de présentation.
    """
    return render(request, 'users/presentation.html', {
        'user': request.user.username if request.user.is_authenticated else None,
    })

@login_required(login_url='/accounts/login/')
def cash_register_page(request):
    # Récupère le profil de l'utilisateur connecté (pour afficher le bon prix)
    user_profile, _ = users_custom.objects.get_or_create(
        user=request.user,
        defaults={
            'first_name': request.user.first_name or 'No Defined',
            'last_name':  request.user.last_name  or 'No Defined',
        }
    )
 
    # Tous les articles et menus
    article_items = Article.objects.all().order_by('type', 'name')
    menu_items    = Menu.objects.all()
 
    # Catégories pour le menu latéral (en dur, correspond aux sections du template)
    categories = ['Tout', 'Menu', 'Le_midi', 'Snack', 'Boisson', 'Viennoiseries']
 
    # Panier stocké en session
    cart  = get_cart(request)
    total = cart_total(cart)
 
    return render(request, 'users/cash_register.html', {
        'article_items': article_items,
        'menu_items':    menu_items,
        'categories':    categories,
        'user_profile':  user_profile,
        'cart':          cart,
        'cart_total':    total,
    })
python manage.py runserver

'''
@login_required(login_url='/accounts/login/')
def cash_register_page(request):
    """
    Page de caisse.
    Affiche les menus et les articles avec le bon prix selon le statut de l'utilisateur.
    """
    user = request.user

    user_data, _ = users_custom.objects.get_or_create(
        user=user,
        defaults={
            'first_name': user.first_name or 'No Defined',
            'last_name': user.last_name or 'No Defined',
        }
    )

    menu_items = [
        {'name': menu.name, 'price': menu.price}
        for menu in Menu.objects.all().order_by('name')
    ]
    cart = get_cart(request) 

    article_items = []
    for article in Article.objects.all().order_by('type', 'name'):
        selected_price = article.price_cotisant if user_data.status == 'cotisant' else article.price_non_cotisant

        article_items.append({
            'name': article.name,
            'type': article.type,
            'quantity': article.quantity,
            'price': selected_price,
            'price_cotisant': article.price_cotisant,
            'price_non_cotisant': article.price_non_cotisant,
        })

    categories = ['Tout', 'Le Midi', 'Boisson', 'Viennoiseries', 'Snack']

    return render(request, 'users/cash_register.html', {
        'user': user.username,
        'user_data': user_data,
        'menu_items': menu_items,
        'article_items': article_items,
        'categories': categories,
        'cart':       cart,          
        'cart_total': cart_total(cart),
    })
'''

@login_required(login_url='/accounts/login/')
def user_dashboard(request):
    """
    Tableau de bord utilisateur.
    Affiche les 5 dernières transactions, les totaux et les statistiques produits.
    """
    user = request.user

    user_data, _ = users_custom.objects.get_or_create(
        user=user,
        defaults={
            'first_name': user.first_name or 'No Defined',
            'last_name': user.last_name or 'No Defined',
        }
    )

    transactions = Transaction.objects.filter(user=user).order_by('-created_at')[:5]

    total_credited = Transaction.objects.filter(user=user, price__gt=0).aggregate(Sum('price'))['price__sum'] or 0
    total_spent = Transaction.objects.filter(user=user, price__lt=0).aggregate(Sum('price'))['price__sum'] or 0

    top_products = (
        TransactionDetails.objects
        .values('article__name')
        .annotate(quantity_sold=Sum('quantity'))
        .order_by('-quantity_sold', 'article__name')[:5]
    )

    categories = ['Accueil', 'Transaction', 'Statistique']
    users = []

    if user_data.role == 'admin':
        categories.append('Administration')
        users = users_custom.objects.select_related('user').all().order_by('user__username')

    return render(request, 'users/user_dashboard.html', {
        'user': user.username,
        'users': users,
        'user_data': user_data,
        'categories': categories,
        'transactions': transactions,
        'total_credited': total_credited,
        'total_spent': abs(total_spent),
        'top_products': top_products,
    })


@login_required(login_url='/accounts/login/')
def update_balance(request):
    """
    Ajoute ou retire du solde à un ou plusieurs utilisateurs.
    Réservé à l'administrateur.
    """
    admin_profile, _ = users_custom.objects.get_or_create(
        user=request.user,
        defaults={
            'first_name': request.user.first_name or 'No Defined',
            'last_name': request.user.last_name or 'No Defined',
        }
    )

    if request.method != 'POST' or admin_profile.role != 'admin':
        messages.error(request, "Accès non autorisé.")
        return redirect('user_dashboard')

    action = request.POST.get('action')
    active_section = request.POST.get('active_section', 'accueil')
    selected_users = request.POST.getlist('selected_users')

    try:
        amount = float(request.POST.get('amount', 0))
    except ValueError:
        messages.error(request, "Montant invalide.")
        return redirect(f"{reverse('user_dashboard')}?active_section={active_section}")

    if amount <= 0:
        messages.error(request, "Le montant doit être supérieur à zéro.")
        return redirect(f"{reverse('user_dashboard')}?active_section={active_section}")

    if action not in ('add', 'subtract'):
        messages.error(request, "Action invalide.")
        return redirect(f"{reverse('user_dashboard')}?active_section={active_section}")

    if not selected_users:
        messages.error(request, "Aucun utilisateur sélectionné.")
        return redirect(f"{reverse('user_dashboard')}?active_section={active_section}")

    updated_count = 0

    for username in selected_users:
        try:
            profile = users_custom.objects.get(user__username=username)

            if action == 'add':
                profile.sold += amount
            else:
                profile.sold -= amount

            profile.save(update_fields=['sold'])
            updated_count += 1

        except users_custom.DoesNotExist:
            messages.error(request, f"L'utilisateur {username} n'existe pas.")

    if updated_count:
        messages.success(request, f"Solde mis à jour pour {updated_count} utilisateur(s).")

    return redirect(f"{reverse('user_dashboard')}?active_section={active_section}")


@login_required(login_url='/accounts/login/')
def send_command_view(request):
    """
    Envoie une commande texte au module Bluetooth de la KFET.
    """
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Mauvaise requête"}, status=400)

    total_price = request.POST.get("total_price", "0")
    address = "98:D3:41:F6:FF:4F"

    try:
        response = send_bluetooth_command(address, f"T:{total_price}€\n")

        if response.startswith("Erreur"):
            return JsonResponse({"status": "error", "response": response}, status=500)

        return JsonResponse({"status": "success", "response": response})

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


# ---------------------------------------------------------------------------
# PANIER EN SESSION
# Les articles cochés dans la caisse sont stockés dans request.session['cart']
# Format : [{"article_id": 5, "name": "Coca", "quantity": 2, "price": 1.50}, ...]
# ---------------------------------------------------------------------------
 
def get_cart(request):
    return request.session.get('cart', [])
 
 
def save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True
 
 
def cart_total(cart):
    return round(sum(item['price'] * item['quantity'] for item in cart), 2)
 
 
@login_required(login_url='/accounts/login/')
def add_to_cart(request):
    """
    Ajoute un article au panier (session).
    Appelé via un formulaire POST depuis cash_register.html.
    """
    if request.method != 'POST':
        return redirect('cash_register_page')
 
    article_id = request.POST.get('article_id')
    quantity   = int(request.POST.get('quantity', 1))
 
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        messages.error(request, "Article introuvable.")
        return redirect('cash_register_page')
 
    # Prix selon le statut de l'utilisateur
    profile, _ = users_custom.objects.get_or_create(user=request.user)
    price = article.price_cotisant if profile.status == 'cotisant' else article.price_non_cotisant
 
    cart = get_cart(request)
 
    # Si l'article est déjà dans le panier, on incrémente
    for item in cart:
        if item['article_id'] == article.pk:
            item['quantity'] += quantity
            save_cart(request, cart)
            messages.success(request, f"Quantité mise à jour : {article.name}")
            return redirect('cash_register_page')
 
    # Sinon on l'ajoute
    cart.append({
        'article_id': article.pk,
        'name':       article.name,
        'quantity':   quantity,
        'price':      price,
    })
    save_cart(request, cart)
    messages.success(request, f"{article.name} ajouté au panier.")
    return redirect('cash_register_page')
 
 
@login_required(login_url='/accounts/login/')
def remove_from_cart(request, article_id):
    """Retire un article du panier."""
    cart = [item for item in get_cart(request) if item['article_id'] != article_id]
    save_cart(request, cart)
    messages.info(request, "Article retiré du panier.")
    return redirect('cash_register_page')
 
 
@login_required(login_url='/accounts/login/')
def clear_cart(request):
    """Vide complètement le panier."""
    save_cart(request, [])
    return redirect('cash_register_page')
 
 
# ---------------------------------------------------------------------------
# ÉTAPE 1 : Lecture NFC + aperçu de la transaction
# ---------------------------------------------------------------------------
 
@login_required(login_url='/accounts/login/')
def nfc_payment_page(request):
    """
    GET : lit la carte NFC et affiche une page de confirmation.
    Si le panier est vide ou que la carte est inconnue, renvoie vers la caisse avec un message.
    """
    cart = get_cart(request)
    total = cart_total(cart)
 
    if not cart:
        messages.warning(request, "Le panier est vide. Ajoutez des articles avant de payer.")
        return redirect('cash_register_page')
 
    # Lecture de la carte
    try:
        uid = read_nfc_uid_once(port=NFC_SERIAL_PORT)
    except (ConnectionError, RuntimeError) as e:
        messages.error(request, f"Erreur du lecteur NFC : {e}")
        return redirect('cash_register_page')
 
    if uid is None:
        messages.warning(request, "Aucune carte détectée. Présentez la carte et réessayez.")
        return redirect('cash_register_page')
 
    # Recherche du profil associé à la carte
    try:
        profile = users_custom.objects.select_related('user').get(nfc_uid=uid)
    except users_custom.DoesNotExist:
        messages.error(request, f"Carte inconnue (UID : {uid}). Demandez à un admin de l'enregistrer.")
        return redirect('cash_register_page')
 
    # Vérification du solde
    solde_insuffisant = profile.sold < total
 
    # On stocke l'UID en session pour la confirmation (évite une 2e lecture)
    request.session['nfc_uid_pending'] = uid
 
    return render(request, 'users/nfc_confirm.html', {
        'profile':            profile,
        'cart':               cart,
        'total':              total,
        'solde_insuffisant':  solde_insuffisant,
    })
 
 
# ---------------------------------------------------------------------------
# ÉTAPE 2 : Confirmation et débit
# ---------------------------------------------------------------------------
 
@login_required(login_url='/accounts/login/')
def nfc_confirm_payment(request):
    """
    POST : valide le paiement après confirmation de l'utilisateur.
    Débite le solde et crée la Transaction en base.
    """
    if request.method != 'POST':
        return redirect('cash_register_page')
 
    uid   = request.session.pop('nfc_uid_pending', None)
    cart  = get_cart(request)
    total = cart_total(cart)
 
    if not uid:
        messages.error(request, "Session expirée. Relancez le paiement NFC.")
        return redirect('cash_register_page')
 
    if not cart:
        messages.error(request, "Le panier est vide.")
        return redirect('cash_register_page')
 
    try:
        profile = users_custom.objects.select_related('user').get(nfc_uid=uid)
    except users_custom.DoesNotExist:
        messages.error(request, "Carte inconnue.")
        return redirect('cash_register_page')
 
    if profile.sold < total:
        messages.error(request, f"Solde insuffisant ({profile.sold:.2f} € disponibles).")
        return redirect('cash_register_page')
 
    # Transaction atomique : tout réussit ou tout est annulé
    try:
        with db_transaction.atomic():
            profile.sold = round(profile.sold - total, 2)
            profile.save(update_fields=['sold'])
 
            txn = Transaction.objects.create(
                user=profile.user,
                price=-total,
            )
 
            for item in cart:
                article = Article.objects.get(pk=item['article_id'])
                TransactionDetails.objects.create(
                    transaction=txn,
                    user=profile.user,
                    article=article,
                    type='vente',
                    quantity=item['quantity'],
                    price=item['price'],
                    payment_type='card',
                )
 
    except Article.DoesNotExist:
        messages.error(request, "Un article du panier est introuvable en base.")
        return redirect('cash_register_page')
    except Exception as e:
        messages.error(request, f"Erreur lors du paiement : {e}")
        return redirect('cash_register_page')
 
    # Panier vidé après paiement
    save_cart(request, [])
 
    messages.success(
        request,
        f"✅ Paiement de {total:.2f} € effectué pour {profile.first_name} {profile.last_name}. "
        f"Nouveau solde : {profile.sold:.2f} €"
    )
    return redirect('cash_register_page')
 
 
# ---------------------------------------------------------------------------
# ASSOCIATION CARTE NFC ↔ COMPTE (admin uniquement)
# ---------------------------------------------------------------------------
 
@login_required(login_url='/accounts/login/')
def nfc_register_view(request):
    """
    GET  : affiche la liste des utilisateurs + les cartes déjà associées.
    POST : lit la carte NFC et l'associe à l'utilisateur sélectionné.
    """
    admin_profile, _ = users_custom.objects.get_or_create(user=request.user)
    if admin_profile.role != 'admin':
        messages.error(request, "Accès réservé aux administrateurs.")
        return redirect('user_dashboard')
 
    all_profiles = users_custom.objects.select_related('user').order_by('last_name')
 
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
 
        try:
            profile = users_custom.objects.select_related('user').get(user__username=username)
        except users_custom.DoesNotExist:
            messages.error(request, f"Utilisateur '{username}' introuvable.")
            return render(request, 'users/nfc_register.html', {'profiles': all_profiles})
 
        try:
            uid = read_nfc_uid_once(port=NFC_SERIAL_PORT)
        except (ConnectionError, RuntimeError) as e:
            messages.error(request, f"Erreur NFC : {e}")
            return render(request, 'users/nfc_register.html', {'profiles': all_profiles})
 
        if uid is None:
            messages.warning(request, "Aucune carte détectée. Présentez la carte et réessayez.")
            return render(request, 'users/nfc_register.html', {'profiles': all_profiles})
 
        # Carte déjà utilisée par quelqu'un d'autre ?
        existing = users_custom.objects.filter(nfc_uid=uid).exclude(pk=profile.pk).first()
        if existing:
            messages.error(
                request,
                f"Cette carte est déjà associée à {existing.first_name} {existing.last_name}."
            )
            return render(request, 'users/nfc_register.html', {'profiles': all_profiles})
 
        profile.nfc_uid = uid
        profile.save(update_fields=['nfc_uid'])
 
        messages.success(
            request,
            f"Carte {uid} associée à {profile.first_name} {profile.last_name}."
        )
        return redirect('nfc_register')
 
    return render(request, 'users/nfc_register.html', {'profiles': all_profiles})


'''
"""
Les Vues (Views) sont les fonctions qui font le travail principal du site.
Elles reçoivent la demande de l'utilisateur, interrogent la base de données, 
et renvoient une page HTML remplie avec les bonnes informations.
"""
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.urls import reverse

from .models import UserCustom, Article, Menu, Transaction, MenuDetails
from .Module_Communication import send_bluetooth_command


def presentation(request):
    return render(request, 'users/présentation.html', {
        'user': request.user.username if request.user.is_authenticated else None,
    })


# Page 1 : KFET : Caisse
@login_required(login_url='/accounts/login/')
def cash_register_page(request):
    users = request.user
    user_data = UserCustom.objects.get(user=users)

    article_data = Article.objects.all()
    menu_data = Menu.objects.all()
    menu_details_data = MenuDetails.objects.all()  # conservé même si non utilisé

    # Menus
    menu_items = []
    for menu in menu_data:
        menu_items.append({'name': menu.name, 'price': menu.price})

    # Articles
    article_items = []
    for article in article_data:
        article_items.append({
            'name': article.name,
            'quantity': article.quantity,
            'type': article.type,
            'price': article.price
        })

    categories = ['Tout', 'Menu', 'Sandwich', 'Snack', 'Boisson']

    return render(request, 'users/cash_register.html', {
        'user': request.user.username,
        'users': users,
        'user_data': user_data,
        'menu_items': menu_items,
        'article_items': article_items,
        'categories': categories,
    })


# Page 2 : Dashboard utilisateur
@login_required(login_url='/accounts/login/')
def user_dashboard(request):
    user = request.user
    user_data, _ = UserCustom.objects.get_or_create(user=user)

    transactions = Transaction.objects.filter(user=user).order_by('-created_at')[:5]
    role = user_data.role

    # Statistiques
    total_credited = Transaction.objects.filter(user=user, price__gt=0)\
        .aggregate(Sum('price'))['price__sum'] or 0

    total_spent = Transaction.objects.filter(user=user, price__lt=0)\
        .aggregate(Sum('price'))['price__sum'] or 0

    top_products = [
        {'name': 'Produit A', 'quantity': 10, 'price': 5.0},
        {'name': 'Produit B', 'quantity': 5, 'price': 10.0},
        {'name': 'Produit C', 'quantity': 2, 'price': 15.0},
    ]

    # Catégories selon rôle
    if role == 'admin':
        categories = ['Accueil', 'Transaction', 'Statistique', 'Administration']
        users = UserCustom.objects.all()
    elif role in ['respo', 'student']:
        categories = ['Accueil', 'Transaction', 'Statistique']
        users = []

    return render(request, 'users/user_dashboard.html', {
        'user': request.user.username,
        'users': users,
        'user_data': user_data,
        'categories': categories,
        'transactions': transactions,
        'total_credited': total_credited,
        'total_spent': abs(total_spent),
        'top_products': top_products,
    })


@login_required
def update_balance(request):
    if request.method == 'POST' and UserCustom.objects.get(user=request.user).role == 'admin':
        action = request.POST.get('action')
        amount = float(request.POST.get('amount', 0))
        selected_users = request.POST.getlist('selected_users')
        active_section = request.POST.get('active_section', 'accueil')

        if not selected_users:
            messages.error(request, "Aucun utilisateur sélectionné.")
            return redirect(f"{reverse('user_dashboard')}?active_section={active_section}")

        for username in selected_users:
            try:
                user = UserCustom.objects.get(user__username=username)

                if action == 'add':
                    user.sold += amount
                elif action == 'subtract':
                    user.sold -= amount

                user.save()
                messages.success(request, f"Le solde de {user.user.username} a été mis à jour.")

            except UserCustom.DoesNotExist:
                messages.error(request, f"L'utilisateur {username} n'existe pas.")
            except ValueError:
                messages.error(request, "Montant invalide.")

        return redirect(f"{reverse('user_dashboard')}?active_section={active_section}")

    return redirect('user_dashboard')


def send_command_view(request):
    """ Vue pour communiquer avec le Bluetooth (JSON). """
    if request.method == "POST":
        try:
            total = request.POST.get("total_price", "0")
            address = "98:D3:41:F6:FF:4F"

            response = send_bluetooth_command(address, f"T:{total}€\n")

            return JsonResponse({
                "status": "success",
                "response": response
            })

        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            })

    return JsonResponse({
        "status": "error",
        "message": "Mauvaise requête"
    }, status=400)


"""
Les Vues (Views) sont les fonctions qui font le travail principal du site.
Elles reçoivent la demande de l'utilisateur, interrogent la base de données, 
et renvoient une page HTML remplie avec les bonnes informations.
"""
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import UserCustom, Article, Menu, Transaction, MenuDetails
from .Module_Communication import send_bluetooth_command

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.db.models import Sum


def presentation(request):
    # Une vue toute simple qui affiche juste une page HTML.
    return render(request, 'users/presentation.html')

def presentation(request):
    return render(request, 'users/présentation.html', {
        'user': request.user.username,
    })

# Le décorateur @login_required oblige l'utilisateur à se connecter (via CAS)
# avant de pouvoir voir cette page. S'il n'est pas connecté, il est renvoyé vers le portail.
@login_required 
def cash_register_page(request):
    """ Affiche la page de la caisse avec tous les articles et menus. """
    # Récupère le profil personnalisé de la personne connectée
    user_prof = UserCustom.objects.get(user=request.user)
    
    # On prépare un "dictionnaire" de données (le context) qu'on va envoyer au fichier HTML.
    # On utilise .values() pour demander à la base de données de nous renvoyer uniquement
    # les noms et les prix. C'est beaucoup plus rapide que de charger tout l'objet.
    context = {
        'user_data': user_prof,
        'menu_items': Menu.objects.all().values('name', 'price'),
        'article_items': Article.objects.all().values('name', 'quantity', 'type', 'price'),
        'categories': ['Tout', 'Menu', 'Sandwich', 'Snack', 'Boisson'],
    }
    # On renvoie la page HTML en lui injectant nos données "context"
    return render(request, 'users/cash_register.html', context)

# Create your views here.
# Page 1 : KFET : Caisse
@login_required(login_url='/accounts/login/')
def cash_register_page(request):
    users = request.user
    user_data = users_custom.objects.get(user=users)  # Récupère tous les utilisateurs
    article_data = Article.objects.all()  # Récupère tous les articles
    menu_data = Menu.objects.all()  # Récupère tous les menus
    menu_details_data = MenuDetails.objects.all()  # Récupère tous les détails de menu

    ## Récupération des menus :
    menu_items = []
    for menu in menu_data:
        menu_items.append({'name': menu.name, 'price': menu.price})
    ## Récupération des articles :
    article_items = []
    for article in article_data:
        article_items.append({'name': article.name, 'quantity': article.quantity,'type': article.type, 'price': article.price})

    ##catégories :
    categories = ['Tout', 'Menu', 'Sandwich', 'Snack', 'Boisson']

    return render (request, 'users/cash_register.html',{
        'user': request.user.username,
        'users': users,
        'user_data': user_data,
        'menu_items': menu_items,
        'article_items': article_items,
        'categories': categories,})


@login_required
def user_dashboard(request):
    """ Affiche le profil de l'utilisateur et son historique d'achats. """
    # get_or_create est une sécurité. Si par hasard le profil n'existe pas, il le crée pour éviter un crash.
    user_prof, created = UserCustom.objects.get_or_create(user=request.user)
    
    # Récupère les 5 dernières transactions de l'utilisateur, classées de la plus récente à la plus ancienne (-created_at)
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    # Calcule l'argent total dépensé. Sum('price') additionne tous les achats (qui sont des valeurs négatives dans la base).
    total_spent = Transaction.objects.filter(user=request.user, price__lt=0).aggregate(Sum('price'))['price__sum'] or 0
    
    context = {
        'user_data': user_prof,
        'transactions': transactions,
        'total_spent': abs(total_spent), # abs() transforme le négatif en positif pour l'affichage
        'categories': ['Accueil', 'Transaction', 'Statistique'],
    }
    
    # Si l'utilisateur est un administrateur, on lui donne accès à des outils supplémentaires
    if user_prof.role == 'admin':
        context['categories'].append('Administration')
        context['all_users'] = UserCustom.objects.all() # Pour gérer les soldes des autres
        
    return render(request, 'users/user_dashboard.html', context)

# Page 2 : Utilisateurs : Gestion des utilisateurs 
@login_required(login_url='/accounts/login/')
def user_dashboard(request):
    user = request.user
    user_data = users_custom.objects.get(user=user)
    transactions = Transaction.objects.filter(user=user).order_by('created_at')[:5]
    role = user_data.role


    #statisitiques 
    total_credited = Transaction.objects.filter(user=user, price__gt=0).aggregate(Sum('price'))['price__sum'] or 0
    total_spent = Transaction.objects.filter(user=user, price__lt=0).aggregate(Sum('price'))['price__sum'] or 0
    top_products = [
        {'name': 'Produit A', 'quantity': 10, 'price': 5.0},
        {'name': 'Produit B', 'quantity': 5, 'price': 10.0},
        {'name': 'Produit C', 'quantity': 2, 'price': 15.0},
    ]
    #catégories en fonction du rôle :
    if role=='admin':
        categories = ['Accueil', 'Transaction', 'Statistique', 'Administration']
        users = users_custom.objects.all()  # Récupère tous les utilisateurs pour l'admin
    elif role=='respo':
        categories = ['Accueil', 'Transaction', 'Statistique']
        users=[]
    elif role=='student':
        categories = ['Accueil', 'Transaction', 'Statistique']
        users=[]

    #Admin :
    #if role=='admin':
        
    return render(request, 'users/user_dashboard.html', {
        'user': request.user.username,
        'users': users,
        'user_data': user_data,
        'categories': categories, 
        'transactions': transactions,
        'total_credited': total_credited,
        'total_spent': total_spent,
        'top_products': top_products,
    })


@login_required
def update_balance(request):
    """ Cette fonction ajoute ou retire de l'argent du solde d'un étudiant. """
    # Sécurité : Uniquement accessible via un formulaire POST, et uniquement par un Admin.
    if request.method == 'POST' and UserCustom.objects.get(user=request.user).role == 'admin':
        action = request.POST.get('action') # "add" (ajouter) ou "subtract" (retirer)
        amount = float(request.POST.get('amount', 0)) # Le montant tapé
        selected_users = request.POST.getlist('selected_users') # La liste des étudiants cochés

        # Pour chaque étudiant sélectionné, on modifie son solde en base de données.
        for username in selected_users:
            try:
                profile = UserCustom.objects.get(user__username=username)
                if action == 'add':
                    profile.sold += amount
                else:
                    profile.sold -= amount
                profile.save() # Enregistre la modification définitivement
            except UserCustom.DoesNotExist:
                pass # Si l'utilisateur n'existe pas, on l'ignore et on passe au suivant
        
        # Envoie un message vert de succès qui s'affichera sur la prochaine page
        messages.success(request, "Soldes mis à jour avec succès.")
    
    # Quoi qu'il arrive, on redirige l'admin vers son tableau de bord
    return redirect('user_dashboard')
def update_balance(request):
    if request.method == 'POST':
        action = request.POST.get('action')  # "add" ou "subtract"
        amount = float(request.POST.get('amount', 0))
        selected_users = request.POST.getlist('selected_users')  # Liste des utilisateurs sélectionnés
        active_section = request.POST.get('active_section', 'accueil')  # Section active 

        if not selected_users:
            messages.error(request, "Aucun utilisateur sélectionné.")
            return redirect(f"{reverse('user_dashboard')}?active_section={active_section}")

        for user_id in selected_users:
            try:
                user = users_custom.objects.get(user__username=user_id)
                print(f"Avant mise à jour : {user.sold}")
                if action == 'add':
                    user.sold += amount
                elif action == 'subtract':
                    user.sold -= amount
                user.save()
                print(f"Après mise à jour : {user.sold}")
                messages.success(request, f"Le solde de {user.first_name} {user.last_name} a été mis à jour.")
            except users_custom.DoesNotExist:
                messages.error(request, f"L'utilisateur avec l'ID {user_id} n'existe pas.")
            except ValueError:
                messages.error(request, "Montant invalide.")

        return redirect(f"{reverse('user_dashboard')}?active_section={active_section}")

def send_command_view(request):
    """ 
    Vue spéciale pour communiquer avec le Bluetooth.
    Elle ne renvoie pas de page HTML, mais une réponse "JSON" (du texte structuré) 
    qui sera lue par le code JavaScript de la caisse.
    """
    if request.method == "POST":
        total = request.POST.get("total_price", "0") # Récupère le prix total cliqué sur la caisse
        address = "98:D3:41:F6:FF:4F" # Adresse MAC de l'afficheur Bluetooth de la KFET
        
        # Appelle notre module indépendant pour envoyer la commande
        response = send_bluetooth_command(address, f"T:{total}€\n")
                try:
            response = send_bluetooth_command(address, command)
            return JsonResponse({"status": "success", "response": response})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Invalid request"})
        # Répond au navigateur pour dire si ça a marché ou non
        return JsonResponse({"status": "success", "response": response})
    
    # Si quelqu'un essaie d'accéder à cette URL sans envoyer de données, on renvoie une erreur 400.
    return JsonResponse({"status": "error", "message": "Mauvaise requête"}, status=400)

    '''