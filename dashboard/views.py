from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

# Create your views here.
@login_required
def home(request):
    return render(request, 'dashboard/home.html')
