# myschool/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
   
    path('accounts/', include('accounts.urls')),
    
    # Optional: redirect root URL to welcome page
    path('', lambda request: redirect('welcome')),  
]
