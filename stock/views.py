from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic import ListView, DeleteView, CreateView, UpdateView, DetailView
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Q
from django_datatables_view.base_datatable_view import BaseDatatableView
from product.models import ProductWarehouse
from stock.forms import ProductWarehouseForm

# Create your views here.
@login_required
def home(request):
    return render(request, 'stock/stock.html')

class StockCreateView(CreateView):
    form_class = ProductWarehouseForm
    model = ProductWarehouse
    success_url = reverse_lazy('stock')
    template_name = 'stock/create.html'
    #fields = ['warehouse', 'product', 'stock', ]

class StockEditView(UpdateView):
    form_class = ProductWarehouseForm
    model = ProductWarehouse
    success_url = reverse_lazy('stock')
    template_name = 'stock/update.html'
    #fields = ['warehouse', 'product', 'stock', ]

class StockDeleteView(DeleteView):
    model = ProductWarehouse
    success_url = reverse_lazy('stock')
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class StockListJson(BaseDatatableView):
    model = ProductWarehouse
    columns = ['warehouse', 'product', 'stock']
    order_columns = ['warehouse', 'product', 'stock']
    max_display_length = 500

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.warehouse.name,
                "%s (%s) %s" % (item.product.name, item.product.size, item.product.color),
                item.stock,
                "<!-- <a href='%s' class='btn btn-sm btn-default'><i class='fa fa-pencil-square-o'></i> Ubah</a> --><a href='#' onclick='javascript: hapus_stok(%s);' class='btn btn-sm btn-danger'><i class='fa fa-trash'></i> Hapus</a>" % (reverse('update_stock', kwargs = {'pk' : item.id, }), item.id)
            ])
        return json_data

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(Q(name__contains=search) | Q(product__name__contains=search))

        return qs