"""
URL configuration for DatabaseDjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users import views
import django_cas_ng.views
from django_cas_ng import views as cas_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', django_cas_ng.views.LoginView.as_view(), name='cas_ng_login'),
    path('accounts/logout/', django_cas_ng.views.LogoutView.as_view(), name='cas_ng_logout'),    
    path('accounts/callback/', django_cas_ng.views.CallbackView.as_view(), name='cas_ng_proxy_callback'),
    path('cash_register_page/',views.cash_register_page, name="cash_register_page"),
    path('',views.user_dashboard, name="user_dashboard"),
    path('update_balance/', views.update_balance, name='update_balance'),
    path('send-command/', views.send_command_view, name='send_command'),
    path('présentation/', views.presentation, name='presentation'),
]
