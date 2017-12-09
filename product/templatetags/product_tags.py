from django import template
from warehouse.models import Warehouse
from product.models import Product, ProductWarehouse
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
register = template.Library()

@register.simple_tag(takes_context=True)
def warehouse(context, product_id, qty_product):
    request = context['request']
    tbl_warehouse = []
    if 'keranjang-penerimaan' in request.session and bool(request.session['keranjang-penerimaan']):
        if str(product_id) in request.session['keranjang-penerimaan']:
            rng = sum(int(x[1]) for x in request.session['keranjang-penerimaan'][str(product_id)]['warehouse'])
            cnt = len(request.session['keranjang-penerimaan'][str(product_id)]['warehouse'])
            product = Product.objects.get(pk=product_id)
            for i in request.session['keranjang-penerimaan'][str(product_id)]['warehouse']:
                warehouse = Warehouse.objects.get(pk=i[0])
                try:
                    product_warehouse = ProductWarehouse.objects.get(product=product, warehouse=warehouse)
                except ProductWarehouse.DoesNotExist:
                    product_warehouse = lambda: None
                    product_warehouse.stock = 0
                    product_warehouse.pk = -1
                if qty_product < rng:
                    i[1] = qty_product/cnt
                tbl_warehouse.append('<tr><input type="hidden" name="warehouse[%s]" value="%s"><td>%s</td><td>%s</td><td class="grid_slider"><input type="text" class="stock-slider2-%s-%s" data-warehouse="%s" data-pk="%s" data-min="0" data-prev="%s" value="%s" name="range[%s][%s]"/></td><td><input type="number" class="form-control stock-input-%s-%s" value="%s"></td></tr>' % (product_id, warehouse.pk, warehouse.name, product_warehouse.stock, product_id, warehouse.pk, warehouse.pk, product.pk, i[1], i[1], product.pk, warehouse.pk, product.pk, warehouse.pk, i[1]))
        else:
            product = Product.objects.get(pk=product_id)
            product_warehouse = ProductWarehouse.objects.filter(product=product)
            tbl_warehouse = []
            for i in product_warehouse:
                qty = int(qty_product)/int(product_warehouse.count())
                tbl_warehouse.append('<tr><input type="hidden" name="warehouse[%s]" value="%s"><td>%s</td><td>%s</td><td class="grid_slider"><input type="text" class="stock-slider2-%s-%s" data-warehouse="%s" data-pk="%s" data-min="0" data-prev="%s" value="%s" name="range[%s][%s]"/></td><td><input type="number" class="form-control stock-input-%s-%s" value="%s"></td></tr>' % (product_id, i.warehouse.pk, i.warehouse.name, i.stock, product_id, i.warehouse.pk, i.warehouse.pk, i.product.pk, qty, qty, i.product.pk, i.warehouse.pk, i.product.pk, i.warehouse.pk, qty))
    else:
        product = Product.objects.get(pk=product_id)
        product_warehouse = ProductWarehouse.objects.filter(product=product)
        tbl_warehouse = []
        for i in product_warehouse:
            qty = int(qty_product)/int(product_warehouse.count())
            tbl_warehouse.append('<tr><input type="hidden" name="warehouse[%s]" value="%s"><td>%s</td><td>%s</td><td class="grid_slider"><input type="text" class="stock-slider2-%s-%s" data-warehouse="%s" data-pk="%s" data-min="0" data-prev="%s" value="%s" name="range[%s][%s]"/></td><td><input type="number" class="form-control stock-input-%s-%s" value="%s"></td></tr>' % (product_id, i.warehouse.pk, i.warehouse.name, i.stock, product_id, i.warehouse.pk, i.warehouse.pk, i.product.pk, qty, qty, i.product.pk, i.warehouse.pk, i.product.pk, i.warehouse.pk, qty))
    
    return mark_safe(''.join(tbl_warehouse))

@register.simple_tag(takes_context=True)
def remain_stock(context, product_id, qty_product):
    request = context['request']
    total = 0
    if 'keranjang-penerimaan' in request.session and bool(request.session['keranjang-penerimaan']):
        if str(product_id) in request.session['keranjang-penerimaan']:
            rng = sum(int(x[1]) for x in request.session['keranjang-penerimaan'][str(product_id)]['warehouse'])
            cnt = len(request.session['keranjang-penerimaan'][str(product_id)]['warehouse'])
        else:
            rng = 0
            cnt = 0
        if str(product_id) in request.session['keranjang-penerimaan']:
            for i in request.session['keranjang-penerimaan'][str(product_id)]['warehouse']:
                if qty_product < rng:
                    i[1] = qty_product/cnt
                total = total + int(i[1])
                pass
        else:
            product = Product.objects.get(pk=product_id)
            product_warehouse = ProductWarehouse.objects.filter(product=product)
            cnt = product_warehouse.count()
            total = (int(qty_product)/int(cnt)) * cnt
    else:
        product = Product.objects.get(pk=product_id)
        product_warehouse = ProductWarehouse.objects.filter(product=product)
        cnt = product_warehouse.count()
        total = (int(qty_product)/int(cnt)) * cnt

    return qty_product - total

@register.simple_tag(takes_context=True)
def warehouse_returned(context, product_id, qty_product):
    request = context['request']
    tbl_warehouse = []
    if 'keranjang-pengembalian' in request.session and bool(request.session['keranjang-pengembalian']):
        if str(product_id) in request.session['keranjang-pengembalian']:
            rng = sum(int(x[1]) for x in request.session['keranjang-pengembalian'][str(product_id)]['warehouse'])
            cnt = len(request.session['keranjang-pengembalian'][str(product_id)]['warehouse'])
            product = Product.objects.get(pk=product_id)
            for i in request.session['keranjang-pengembalian'][str(product_id)]['warehouse']:
                warehouse = Warehouse.objects.get(pk=i[0])
                try:
                    product_warehouse = ProductWarehouse.objects.get(product=product, warehouse=warehouse)
                except ProductWarehouse.DoesNotExist:
                    product_warehouse = lambda: None
                    product_warehouse.stock = 0
                    product_warehouse.pk = -1
                if qty_product < rng:
                    i[1] = product_warehouse.stock
                tbl_warehouse.append('<tr><input type="hidden" name="warehouse[%s]" value="%s"><td>%s</td><td>%s</td><td class="grid_slider"><input type="text" class="stock-slider2-%s-%s" data-warehouse="%s" data-pk="%s" data-min="0" data-prev="%s" value="%s" name="range[%s][%s]"/></td><td><input type="number" class="form-control stock-input-%s-%s" value="%s"></td></tr>' % (product_id, warehouse.pk, warehouse.name, product_warehouse.stock, product_id, warehouse.pk, warehouse.pk, product.pk, i[1], i[1], product.pk, warehouse.pk, product.pk, warehouse.pk, i[1]))
        else:
            product = Product.objects.get(pk=product_id)
            product_warehouse = ProductWarehouse.objects.filter(product=product)
            tbl_warehouse = []
            for i in product_warehouse:
                qty = i.stock
                tbl_warehouse.append('<tr><input type="hidden" name="warehouse[%s]" value="%s"><td>%s</td><td>%s</td><td class="grid_slider"><input type="text" class="stock-slider2-%s-%s" data-warehouse="%s" data-pk="%s" data-min="0" data-prev="%s" value="%s" name="range[%s][%s]"/></td><td><input type="number" class="form-control stock-input-%s-%s" value="%s"></td></tr>' % (product_id, i.warehouse.pk, i.warehouse.name, i.stock, product_id, i.warehouse.pk, i.warehouse.pk, i.product.pk, qty, qty, i.product.pk, i.warehouse.pk, i.product.pk, i.warehouse.pk, qty))
    else:
        product = Product.objects.get(pk=product_id)
        product_warehouse = ProductWarehouse.objects.filter(product=product)
        tbl_warehouse = []
        for i in product_warehouse:
            qty = i.stock
            tbl_warehouse.append('<tr><input type="hidden" name="warehouse[%s]" value="%s"><td>%s</td><td>%s</td><td class="grid_slider"><input type="text" class="stock-slider2-%s-%s" data-warehouse="%s" data-pk="%s" data-min="0" data-prev="%s" value="%s" name="range[%s][%s]"/></td><td><input type="number" class="form-control stock-input-%s-%s" value="%s"></td></tr>' % (product_id, i.warehouse.pk, i.warehouse.name, i.stock, product_id, i.warehouse.pk, i.warehouse.pk, i.product.pk, qty, qty, i.product.pk, i.warehouse.pk, i.product.pk, i.warehouse.pk, qty))
    
    return mark_safe(''.join(tbl_warehouse))

@register.simple_tag(takes_context=True)
def remain_stock_returned(context, product_id, qty_product):
    request = context['request']
    total = 0
    if 'keranjang-pengembalian' in request.session and bool(request.session['keranjang-pengembalian']):
        if str(product_id) in request.session['keranjang-pengembalian']:
            rng = sum(int(x[1]) for x in request.session['keranjang-pengembalian'][str(product_id)]['warehouse'])
            cnt = len(request.session['keranjang-pengembalian'][str(product_id)]['warehouse'])
        else:
            rng = 0
            cnt = 0
        if str(product_id) in request.session['keranjang-pengembalian']:
            for i in request.session['keranjang-pengembalian'][str(product_id)]['warehouse']:
                if qty_product < rng:
                    i[1] = qty_product
                total = total + int(i[1])
                pass
        else:
            product = Product.objects.get(pk=product_id)
            product_warehouse = ProductWarehouse.objects.filter(product=product)
            cnt = product_warehouse.count()
            #total = (int(qty_product)/int(cnt)) * cnt
            total = int(qty_product)
    else:
        product = Product.objects.get(pk=product_id)
        product_warehouse = ProductWarehouse.objects.filter(product=product)
        cnt = product_warehouse.count()
        #total = (int(qty_product)/int(cnt)) * cnt
        total = int(qty_product)

    return qty_product - total

@register.simple_tag(takes_context=True)
def cart_total_returnded(context):
    request = context['request']
    total = 0
    '''if 'keranjang-pengembalian' in request.session and bool(request.session['keranjang-pengembalian']):
        if str(product_id) in request.session['keranjang-pengembalian']:
            rng = sum(int(x[1]) for x in request.session['keranjang-pengembalian'][str(product_id)]['warehouse'])
            cnt = len(request.session['keranjang-pengembalian'][str(product_id)]['warehouse'])
        else:
            rng = 0
            cnt = 0
        if str(product_id) in request.session['keranjang-pengembalian']:
            for i in request.session['keranjang-pengembalian'][str(product_id)]['warehouse']:
                if qty_product < rng:
                    i[1] = qty_product
                total = total + int(i[1])
    {u'2': {u'warehouse': [[u'2', u'2'], [u'1', u'0'], [u'4', u'0']], u'range': [u'2', u'0', u'0'], u'remain': u'0'}}
    '''
    print request.session['keranjang-pengembalian']
    for i in request.session['keranjang-pengembalian']:
        product = Product.objects.get(pk=i)
        for x in request.session['keranjang-pengembalian'][i]['range']:
            total = total + (product.cost_price * float(x))

    return "Rp. %s" % total