from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
@login_required
def err_permmision(request):
    return render(request, 'account/error_permmision.html')