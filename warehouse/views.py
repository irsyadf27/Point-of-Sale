from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DeleteView, CreateView, UpdateView, DetailView
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy, reverse
from django_datatables_view.base_datatable_view import BaseDatatableView
from warehouse.models import Warehouse
from warehouse.forms import WarehouseForm
from product.models import ProductWarehouse, Product
import json

# Create your views here.
@login_required
def home(request):
    return render(request, 'warehouse/warehouse.html')

class WarehouseDetailView(DetailView):
    model = Warehouse
    template_name = 'warehouse/detail.html'

class WarehouseCreateView(CreateView):
    form_class = WarehouseForm
    model = Warehouse
    success_url = reverse_lazy('warehouse')
    template_name = 'warehouse/create.html'
    #fields = ['name', 'address', 'phone', ]

class WarehouseEditView(UpdateView):
    form_class = WarehouseForm
    model = Warehouse
    success_url = reverse_lazy('warehouse')
    template_name = 'warehouse/update.html'
    #fields = ['name', 'address', 'phone', ]

class WarehouseDeleteView(DeleteView):
    model = Warehouse
    success_url = reverse_lazy('warehouse')
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
        
class WarehouseListJson(BaseDatatableView):
    model = Warehouse
    columns = ['name', 'address', 'phone']
    order_columns = ['name', 'address']
    max_display_length = 500

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.name,
                item.address,
                item.phone,
                item.num_of_products,
                "<a href='%s' class='btn btn-sm btn-primary'><i class='fa fa-cube'></i> Produk</a><a href='%s' class='btn btn-sm btn-default'><i class='fa fa-pencil-square-o'></i> Ubah</a> <a href='#' onclick='javascript: hapus_gudang(%s);' class='btn btn-sm btn-danger'><i class='fa fa-trash'></i> Hapus</a>" % (reverse('detail_warehouse', kwargs = {'pk' : item.id, }), reverse('update_warehouse', kwargs = {'pk' : item.id, }), item.id)
            ])
        return json_data
        
    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(name__contains=search)

        return qs

class WarehouseProductListJson(BaseDatatableView):
    model = ProductWarehouse
    columns = ['product', 'stock', ]
    order_columns = ['product', 'stock', ]
    max_display_length = 500

    def get_initial_queryset(self):
        qs = ProductWarehouse.objects.filter(warehouse=self.kwargs['pk'])
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                "%s (%s) %s" % (item.product.name, item.product.size, item.product.color),
                item.stock,
                "<a href='%s' class='btn btn-sm btn-default'><i class='fa fa-pencil-square-o'></i> Ubah Stok</a>" % (reverse('update_stock', kwargs = {'pk' : item.id, })),
            ])
        return json_data

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(product__name__contains=search)

        return qs

@login_required
def list_warehouse(request, pk):
    result = []
    if 'keranjang-penerimaan' in request.session and bool(request.session['keranjang-penerimaan']) and str(pk) in request.session['keranjang-penerimaan']:
        list_warehouse = [i[0] for i in request.session['keranjang-penerimaan'][str(pk)]['warehouse']]
    else:
        product = Product.objects.get(pk=pk)
        list_warehouse = [i.warehouse.pk for i in ProductWarehouse.objects.filter(product=product)]
    qs = Warehouse.objects.exclude(pk__in=list_warehouse)
    for data in qs:
        result.append({'id': data.pk, 'text': str(data)})
    result = json.dumps({'results': result})
    return HttpResponse(result, content_type='application/json')