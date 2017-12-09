from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy, reverse
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.views.decorators.csrf import csrf_exempt
from product.models import Product, ProductWarehouse
from received_product.forms import ReceiveProductForm
from received_product.models import ReceivedProduct, ReceivedProductDetail
from warehouse.models import Warehouse
from carton.cart import Cart
import json

class ReceiveProductView(CreateView):
    form_class = ReceiveProductForm
    model = ProductWarehouse
    success_url = reverse_lazy('receive_product')
    template_name = 'received_product/receive.html'

@login_required
def add(request, pk):
    '''sess = request.session.exists('list_product')
    if not sess:
        data = get_object_or_404(Product, pk=1)
        obj = {
            'id': data.id, 
            'name': data.name, 
            'cost_price': data.cost_price, 
            'selling_price': data.selling_price, 
            'stock': ProductWarehouse.objects.filter(product=data).first().stock, 
            'qty': 0
        }
        request.session['list_product'] = [obj]
    else:
        list_sess = request.session.get('list_product')
        add_stock = request.POST.get('stock', None)
        if add_stock:
            pass
        list_sess.append(obj)
        request.session['list_product'] = list_sess
    print request.session.get('list_product')
    return HttpResponse('test')'''

    cart = Cart(request.session, session_key='CART-RECEIVE-PRODUCT')
    product = Product.objects.get(id=pk)
    cart.add(product, price=product.cost_price)
    return HttpResponse("Added")

@login_required
def remove_cart(request, pk):
    cart = Cart(request.session, session_key='CART-RECEIVE-PRODUCT')
    product = Product.objects.get(id=pk)
    cart.remove(product)
    return HttpResponse("Removed")

@login_required
def set_qty(request, pk):
    cart = Cart(request.session, session_key='CART-RECEIVE-PRODUCT')
    product = Product.objects.get(id=pk)
    cart.set_quantity(product, request.POST.get('value', 0))
    res = {'pk': pk, 'qty':request.POST.get('value', 0), 'price': product.cost_price * float(request.POST.get('value', 0))}
    return HttpResponse(json.dumps(res), content_type='application/json')

@login_required
def show_cart(request):
    return render(request, 'received_product/receive/table.html')

@login_required
def cart_total(request):
    return render(request, 'received_product/receive/total.html')

class ItemKeranjang(object):
    def __init__(self, warehouse, range, remain):
        self.warehouse = warehouse
        self.range = range
        self.remain = remain

    def to_dict(self):
        list_warehouse = {}
        for idx, item in self.warehouse:
            list_warehouse[item.pk] = {'warehouse': item, 'range': self.range[idx]}

        return list_warehouse

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
        request.session['keranjang-penerimaan'] = arr
    return HttpResponse(arr)

@login_required
@csrf_exempt
def checkout(request):
    cart = Cart(request.session, session_key='CART-RECEIVE-PRODUCT')
    product = request.POST.getlist('product')
    if product:
        received = ReceivedProduct(
            actor=request.user,
            qty=cart.count,
            total=cart.total,
            )
        received.save()
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
                received_detail = ReceivedProductDetail(
                    received_product=received,
                    product_warehouse=obj_warehouse,
                    qty=z[1],
                    subtotal=obj_product.cost_price * float(z[1])
                    )
                received_detail.save()
                obj_warehouse.stock = obj_warehouse.stock + int(z[1])
                obj_warehouse.save()
    cart.clear()
    return HttpResponse("Success")