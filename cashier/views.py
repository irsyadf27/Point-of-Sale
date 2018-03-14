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
from product.models import Product, ProductWarehouse
from warehouse.models import Warehouse
from cashier.models import Invoice, InvoiceDetail

# Create your views here.
@login_required
def home(request):
    form = CashierForm()
    return render(request, 'cashier/cashier.html', {'form': form})

class InvoiceView(DetailView):
    model = Invoice
    template_name = 'cashier/invoice.html'
    slug_field = 'invoice_number'
    slug_url_kwarg = 'invoice_number'
    query_pk_and_slug = True


@login_required
def mapping(request):
    return render(request, 'cashier/mapping-gudang.html')

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
    if request.session.get('keranjang-cashier', None):
        if request.session['keranjang-cashier'].get('pk', None):
            del request.session['keranjang-cashier'][pk]
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
        request.session['keranjang-cashier'] = arr
    return HttpResponse(arr)


@login_required
@csrf_exempt
def checkout(request):
    product = request.POST.getlist('produk')
    cart = Cart(request.session, session_key='CART-CASHIER-PRODUCT')
    for i in product:
        invoice = Invoice(
            cashier=request.user,
            qty=cart.count,
            total=cart.total,
            )
        invoice.save()

        gudang = request.POST.getlist('gudang[' + str(i) + ']')
        for g in gudang:
            gdg = g.split('-')
            obj_wh = Warehouse.objects.get(pk=gdg[0])
            obj_product = Product.objects.get(pk=i)
            obj_warehouse = ProductWarehouse.objects.get(product=obj_product, warehouse=obj_wh)
            obj_warehouse.stock = obj_warehouse.stock - int(gdg[1])
            obj_warehouse.save()

            invoice_detail = InvoiceDetail(
                invoice=invoice,
                product_warehouse=obj_warehouse,
                qty=int(gdg[1]),
                price=obj_product.selling_price,
                subtotal=obj_product.selling_price * float(int(gdg[1]))
                )
            invoice_detail.save()
        if request.session.get('keranjang-cashier', None):
            del request.session['keranjang-cashier']
        cart.clear()
        return redirect(reverse_lazy('invoice_detail', kwargs={'invoice_number': invoice.invoice_number}))