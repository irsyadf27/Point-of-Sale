from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Q, Sum
from customer_return.forms import CustomerReturnForm
from customer_return.models import Retur, ReturDetail
from config.models import Config
from cashier.models import Invoice
from product.models import Product, ProductWarehouse
from warehouse.models import Warehouse
from carton.cart import Cart

# Create your views here.
@login_required
def home(request):
    cart = Cart(request.session, session_key='CART-RETURN-CUSOMER')
    cart.clear()
    cart2 = Cart(request.session, session_key='CART-RETURN-CUSOMER2')
    cart2.clear()
    if 'keranjang-customer-return' in request.session:
        del request.session['keranjang-customer-return']

    form = CustomerReturnForm()
    return render(request, 'customer_return/return.html', {'form': form})

@login_required
def get_invoice(request, invoice_number):
    try:
        invoice = Invoice.objects.get(invoice_number=invoice_number)
    except Invoice.DoesNotExist:
        return HttpResponse('error')

    cart = Cart(request.session, session_key='CART-RETURN-CUSOMER')
    cart.clear()
    cart2 = Cart(request.session, session_key='CART-RETURN-CUSOMER2')
    cart2.clear()
    if 'keranjang-customer-return' in request.session:
        del request.session['keranjang-customer-return']

    conf = Config.objects.first()
    for produk in invoice.details.all():
        product = Product.objects.get(id=produk.product_warehouse.product.pk)
        qty = ReturDetail.objects.filter(Q(product_warehouse__product=product) & Q(retur__invoice=invoice)).aggregate(Sum('qty'))['qty__sum']
        if qty is None:
            qty = 0

        if produk.qty - qty > 0:
            cart.add(product, price=(product.selling_price - conf.potongan), quantity=(produk.qty - qty))

    return HttpResponse('sukses')

@login_required
def set_qty(request, pk):
    cart = Cart(request.session, session_key='CART-RETURN-CUSOMER')
    product = Product.objects.get(id=pk)
    cart.set_quantity(product, request.POST.get('value', 0))
    res = {'pk': pk, 'qty':request.POST.get('value', 0)}
    return HttpResponse(json.dumps(res), content_type='application/json')

@login_required
def show_cart(request):
    return render(request, 'customer_return/table.html')

@login_required
def cart_total(request):
    return render(request, 'customer_return/total.html')

@login_required
@csrf_exempt
def testpost(request):
    conf = Config.objects.first()
    cart = Cart(request.session, session_key='CART-RETURN-CUSOMER2')
    product = request.POST.getlist('product')
    arr = {}
    if product:
        for i in product:
            product = Product.objects.get(id=i)
            warehouse = request.POST.getlist('warehouse[%s]' % i)
            remain = request.POST.get('sisa[%s]' % i)
            list_range = []
            for x in warehouse:
                rng = request.POST.get('range[%s][%s]' % (i, x))
                list_range.append(rng)

            total_range = sum([int(rng) for rng in list_range])
            if total_range > 0:
                if cart.__contains__(product):
                    cart.set_quantity(product, total_range)
                else:
                    cart.add(product, price=(product.selling_price - conf.potongan), quantity=total_range)
            list_warehouse = zip(warehouse, list_range)
            arr[i] = {'warehouse': list_warehouse, 'range': list_range, 'remain': remain}
        request.session['keranjang-customer-return'] = arr
    return HttpResponse(arr)

@login_required
@csrf_exempt
def checkout(request):
    cart = Cart(request.session, session_key='CART-RETURN-CUSOMER2')
    product = request.POST.getlist('product')
    invoice_number = request.POST.get('invoice_number')
    invoice = Invoice.objects.get(invoice_number=invoice_number)
    conf = Config.objects.first()
    if product:

        retur = Retur(
            invoice=invoice,
            cashier=request.user,
            qty=cart.count,
            total=cart.total,
            potongan=conf.potongan
            )
        retur.save()
        for i in product:
            obj_product = Product.objects.get(pk=i)
            warehouse = request.POST.getlist('warehouse[%s]' % i)
            remain = request.POST.get('sisa[%s]' % i)
            list_range = []
            for x in warehouse:
                list_range.append(request.POST.get('range[%s][%s]' % (i, x)))
            list_warehouse = zip(warehouse, list_range)

            for z in list_warehouse:
                obj_wh = Warehouse.objects.get(pk=int(z[0]))
                obj_warehouse, created = ProductWarehouse.objects.get_or_create(product=obj_product, warehouse=obj_wh, defaults={'stock': int(z[1])})
                if int(z[1]) > 0:
                    retur_detail = ReturDetail(
                        retur=retur,
                        product_warehouse=obj_warehouse,
                        qty=z[1],
                        selling_price=obj_product.selling_price,
                        subtotal=(obj_product.selling_price - conf.potongan) * float(z[1])
                        )
                    retur_detail.save()
                if not created:
                    obj_warehouse.stock = obj_warehouse.stock + int(z[1])
                    obj_warehouse.save()
                    
    if 'keranjang-customer-return' in request.session:
        del request.session['keranjang-customer-return']      
    cart.clear()
    cart2 = Cart(request.session, session_key='CART-RETURN-CUSOMER2')
    cart2.clear()
    return HttpResponse("Success")