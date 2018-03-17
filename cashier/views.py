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
from discount.models import Discount
from customer.models import Customer

# Create your views here.
@login_required
def home(request):
    form = CashierForm()
    discount = Discount.objects.all()
    cart = Cart(request.session, session_key='CART-CASHIER-PRODUCT')
    if request.session.get('keranjang-cashier', None):
        del request.session['keranjang-cashier']
    if request.session.get('discount', None):
        del request.session['discount']
    if request.session.get('discount_pk', None):
        del request.session['discount_pk']
    if request.session.get('pelanggan', None):
        del request.session['pelanggan']
    cart.clear()
    return render(request, 'cashier/cashier.html', {'form': form, 'discount': discount})

class InvoiceView(DetailView):
    model = Invoice
    template_name = 'cashier/invoice.html'
    slug_field = 'invoice_number'
    slug_url_kwarg = 'invoice_number'
    query_pk_and_slug = True

@login_required
def set_pelanggan(request, pk):
    request.session['pelanggan'] = int(pk)
    return HttpResponse(str(pk))

@login_required
def set_discount(request, pk):
    cart = Cart(request.session, session_key='CART-CASHIER-PRODUCT')
    discount = Discount.objects.get(pk=pk)
    total = 0
    if discount.discount_type == 'percent':
        total = float(cart.total) * (float(discount.discount_value) / 100)
    else:
        total = float(discount.discount_value)
    request.session['discount'] = total
    request.session['discount_pk'] = int(pk)
    return HttpResponse(str(total))

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
    current_qty = 0
    max_stock = product.stock
    if cart._items_dict.get(int(product_id), None):
        current_qty = cart._items_dict[int(product_id)].quantity

    if max_stock == 0:
        return HttpResponse(json.dumps({'error': 1, 'msg': 'Stok tidak mencukupi', 'max': max_stock}), content_type='application/json')

    if (current_qty + int(qty)) > max_stock:
        if cart.__contains__(product):
            cart.set_quantity(product, max_stock)
        else:
            cart.add(product, price=product.selling_price, quantity=max_stock)
        return HttpResponse(json.dumps({'error': 1, 'msg': 'Stok tidak mencukupi', 'max': max_stock}), content_type='application/json')


    cart.add(product, price=product.selling_price, quantity=qty)
    return HttpResponse(json.dumps({'error': 0, 'msg': 'sukses'}), content_type='application/json')

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
    qty = request.POST.get('value', 0)
    product = Product.objects.get(id=pk)
    max_stock = product.stock

    if max_stock == 0:
        return HttpResponse(json.dumps({'error': 1, 'msg': 'Stok tidak mencukupi', 'max': max_stock}), content_type='application/json')

    if int(qty) > max_stock:
        cart.set_quantity(product, max_stock)
        return HttpResponse(json.dumps({'error': 1, 'msg': 'Stok tidak mencukupi', 'max': max_stock}), content_type='application/json')
    cart.set_quantity(product, qty)
    res = {'pk': pk, 'qty': qty, 'price': product.selling_price * float(qty)}
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
    customer = None
    discount = None
    discount_size = 0
    cost_total = 0
    if request.session.get('pelanggan', None):
        customer = Customer.objects.get(pk=request.session['pelanggan'])
    if request.session.get('discount', None):
        discount = Discount.objects.get(pk=request.session['discount_pk'])
        if discount.discount_type == 'percent':
            discount_size = float(cart.total) * (float(discount.discount_value) / 100)
        else:
            discount_size = float(discount.discount_value)
    invoice = Invoice(
        cashier=request.user,
        qty=cart.count,
        total=cart.total,
        discount_size=discount_size,
        customer=customer,
        discount=discount
        )
    invoice.save()
    for i in product:
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
                cost_price=obj_product.cost_price,
                selling_price=obj_product.selling_price,
                subtotal=obj_product.selling_price * float(int(gdg[1]))
                )
            invoice_detail.save()
            cost_total += obj_product.cost_price * float(int(gdg[1]))
        if request.session.get('keranjang-cashier', None):
            del request.session['keranjang-cashier']
        if request.session.get('discount', None):
            del request.session['discount']
        if request.session.get('discount_pk', None):
            del request.session['discount_pk']
        if request.session.get('pelanggan', None):
            del request.session['pelanggan']
        cart.clear()
        invoice.cost_total = cost_total
        invoice.save()
        return redirect(reverse_lazy('invoice_detail', kwargs={'invoice_number': invoice.invoice_number}))