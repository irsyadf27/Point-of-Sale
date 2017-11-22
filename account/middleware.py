from django.contrib.auth.views import redirect_to_login
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy

class AllowSuperUserOnly(MiddlewareMixin):
    def process_request(self, request):
        path = ('/accounts/create/', '/accounts/create/', '/accounts/update/', '/accounts/data/'
            '/customer/', '/discount/', '/merk/', '/product/', 
            '/warehouse/', '/stock/'
            )
        if request.path.startswith(path):
            if not request.user.is_superuser:
                return redirect(reverse_lazy('err_permmision'))
        return None