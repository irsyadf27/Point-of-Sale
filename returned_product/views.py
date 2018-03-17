from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import CreateView, DetailView
from django.core.urlresolvers import reverse_lazy, reverse
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.views.decorators.csrf import csrf_exempt
from product.models import Product, ProductWarehouse
from returned_product.forms import ReturnedProductForm
from returned_product.models import ReturnedProduct, ReturnedProductDetail
from warehouse.models import Warehouse
from carton.cart import Cart
import json

# Create your views here.
class ReturnedProductView(CreateView):
    form_class = ReturnedProductForm
    model = ProductWarehouse
    success_url = reverse_lazy('returned:returned_product')
    template_name = 'returned_product/return.html'

@login_required
def add(request, pk):
    cart = Cart(request.session, session_key='CART-RETURN-PRODUCT')
    product = Product.objects.get(id=pk)
    cart.add(product, price=product.cost_price)
    cart.set_quantity(product, product.stock)
    return HttpResponse("Added")

@login_required
def remove_cart(request, pk):
    cart = Cart(request.session, session_key='CART-RETURN-PRODUCT')
    product = Product.objects.get(id=pk)
    if 'keranjang-pengembalian' in request.session:
        if pk in request.session['keranjang-pengembalian']:
            del request.session['keranjang-pengembalian'][pk]
    cart.remove(product)
    return HttpResponse("Removed")

@login_required
def set_qty(request, pk):
    cart = Cart(request.session, session_key='CART-RETURN-PRODUCT')
    product = Product.objects.get(id=pk)
    cart.set_quantity(product, request.POST.get('value', 0))
    res = {'pk': pk, 'qty':request.POST.get('value', 0), 'price': product.cost_price * float(request.POST.get('value', 0))}
    return HttpResponse(json.dumps(res), content_type='application/json')

@login_required
def show_cart(request):
    return render(request, 'returned_product/return/table.html')

@login_required
def cart_total(request):
    return render(request, 'returned_product/return/total.html')

@login_required
@csrf_exempt
def testpost(request):
    product = request.POST.getlist('product')
    arr = {}
    if product:
        for i in product:
            warehouse = request.POST.getlist('warehouse[%s]' % i)
            remain = request.POST.get('sisa[%s]' % i)
            list_range = []
            for x in warehouse:
                list_range.append(request.POST.get('range[%s][%s]' % (i, x)))
            list_warehouse = zip(warehouse, list_range)
            arr[i] = {'warehouse': list_warehouse, 'range': list_range, 'remain': remain}
        request.session['keranjang-pengembalian'] = arr
    return HttpResponse(arr)

@login_required
@csrf_exempt
def checkout(request):
    cart = Cart(request.session, session_key='CART-RETURN-PRODUCT')
    product = request.POST.getlist('product')
    if product:
        returned = ReturnedProduct(
            actor=request.user,
            qty=cart.count,
            total=cart.total,
            )
        returned.save()
        for i in product:
            obj_product = Product.objects.get(pk=i)
            warehouse = request.POST.getlist('warehouse[%s]' % i)
            remain = request.POST.get('sisa[%s]' % i)
            list_range = []
            for x in warehouse:
                list_range.append(request.POST.get('range[%s][%s]' % (i, x)))
            list_warehouse = zip(warehouse, list_range)
            for z in list_warehouse:
                obj_wh = Warehouse.objects.get(pk=z[0])
                obj_warehouse, created = ProductWarehouse.objects.get_or_create(product=obj_product, warehouse=obj_wh, defaults={'stock': 0})
                returned_detail = ReturnedProductDetail(
                    returned_product=returned,
                    product_warehouse=obj_warehouse,
                    qty=z[1],
                    subtotal=obj_product.cost_price * float(z[1])
                    )
                returned_detail.save()
                obj_warehouse.stock = int(z[1])
                obj_warehouse.save()

    if 'keranjang-pengembalian' in request.session:
        del request.session['keranjang-pengembalian'] 

    cart.clear()
    return HttpResponse("Success")