from django.shortcuts import render
from django.http import JsonResponse
from .models import users_custom
from .models import Article
from .models import Menu
from .models import MenuDetails
from .models import Transaction
from .Module_Communication import send_bluetooth_command

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.db.models import Sum

def presentation(request):
    return render(request, 'users/présentation.html', {
        'user': request.user.username,
    })



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
    if request.method == "POST":
        total_price = request.POST.get("total_price", "0")
        command = f"Total: {total_price} € /r/n"  
        address = "98:D3:41:F6:FF:4F"  # Adresse MAC du HC-05
        try:
            response = send_bluetooth_command(address, command)
            return JsonResponse({"status": "success", "response": response})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Invalid request"})