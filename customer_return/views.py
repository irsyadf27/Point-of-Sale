from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, HttpResponse
from customer_return.forms import CustomerReturnForm
from customer_return.models import Retur, ReturDetail
from config.models import Config
from cashier.models import Invoice
from product.models import Product, ProductWarehouse
from carton.cart import Cart

# Create your views here.
@login_required
def home(request):
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
    if 'keranjang-customer-return' in request.session:
        del request.session['keranjang-customer-return'] 
    conf = Config.objects.first()
    for produk in invoice.details.all():
        product = Product.objects.get(id=produk.product_warehouse.product.pk)
        cart.add(product, price=(product.selling_price - conf.potongan), quantity=produk.qty)

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
        request.session['keranjang-customer-return'] = arr
    return HttpResponse(arr)

@login_required
@csrf_exempt
def checkout(request):
    cart = Cart(request.session, session_key='CART-RETURN-CUSOMER')
    product = request.POST.getlist('product')
    invoice_number = request.POST.get('invoice_number')
    invoice = Invoice.objects.get(invoice_number=invoice_number)
    conf = Config.objects.first()
    if product:
        retur = Retur(
            invoice=invoice,
            actor=request.user,
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
                retur_detail = ReturDetail(
                    retur=retur,
                    product_warehouse=obj_warehouse,
                    qty=z[1],
                    subtotal=(obj_product.selling_price - conf.potongan) * float(z[1])
                    )
                retur_detail.save()
                if not created:
                    obj_warehouse.stock = obj_warehouse.stock + int(z[1])
                    obj_warehouse.save()
                    
    if 'keranjang-customer-return' in request.session:
        del request.session['keranjang-customer-return']      
    cart.clear()
    return HttpResponse("Success")