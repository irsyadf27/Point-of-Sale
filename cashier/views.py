from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DeleteView, CreateView, UpdateView, DetailView
from django.core.urlresolvers import reverse_lazy, reverse
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.views.decorators.csrf import csrf_exempt
from carton.cart import Cart
import json
from cashier.forms import CashierForm
from product.models import Product

# Create your views here.
@login_required
def home(request):
    form = CashierForm()
    return render(request, 'cashier/cashier.html', {'form': form})


@login_required
@csrf_exempt
def add(request):
    product_id = request.POST.get('produk', None)
    qty = request.POST.get('qty', 1)
    qrcode = request.POST.get('qrcode', None)
    if qrcode:
        product = Product.objects.get(qrcode=qrcode)
    else:
        product = Product.objects.get(id=product_id)
    cart = Cart(request.session, session_key='CART-CASHIER-PRODUCT')
    cart.add(product, price=product.selling_price, quantity=qty)
    return HttpResponse("Added")

@login_required
def remove_cart(request, pk):
    cart = Cart(request.session, session_key='CART-CASHIER-PRODUCT')
    product = Product.objects.get(id=pk)
    cart.remove(product)
    return HttpResponse("Removed")

@login_required
def set_qty(request, pk):
    cart = Cart(request.session, session_key='CART-CASHIER-PRODUCT')
    product = Product.objects.get(id=pk)
    cart.set_quantity(product, request.POST.get('value', 0))
    res = {'pk': pk, 'qty':request.POST.get('value', 0), 'price': product.selling_price * float(request.POST.get('value', 0))}
    return HttpResponse(json.dumps(res), content_type='application/json')

@login_required
def show_cart(request):
    return render(request, 'cashier/table.html')

@login_required
def cart_total(request):
    return render(request, 'returned_product/return/total.html')