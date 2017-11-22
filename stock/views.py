from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic import ListView, DeleteView, CreateView, UpdateView, DetailView
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Q
from django_datatables_view.base_datatable_view import BaseDatatableView
from product.models import ProductWarehouse

# Create your views here.
@login_required
def home(request):
    return render(request, 'stock/stock.html')

class StockCreateView(CreateView):
    model = ProductWarehouse
    success_url = reverse_lazy('stock')
    template_name = 'stock/create.html'
    fields = ['warehouse', 'product', 'stock', ]

class StockEditView(UpdateView):
    model = ProductWarehouse
    success_url = reverse_lazy('stock')
    template_name = 'stock/update.html'
    fields = ['warehouse', 'product', 'stock', ]

class StockDeleteView(DeleteView):
    model = ProductWarehouse
    success_url = reverse_lazy('stock')
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class StockListJson(BaseDatatableView):
    # The model we're going to show
    model = ProductWarehouse

    # define the columns that will be returned
    columns = ['warehouse', 'product', 'stock']

    # define column names that will be used in sorting
    # order is important and should be same as order of columns
    # displayed by datatables. For non sortable columns use empty
    # value like ''
    order_columns = ['warehouse', 'product', 'stock']

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 500

    #def render_column(self, row, column):
    #    return super(StockListJson, self).render_column(row, column)

    def prepare_results(self, qs):
        # prepare list with output column data
        # queryset is already paginated here
        json_data = []
        for item in qs:
            json_data.append([
                item.warehouse.name,
                "%s (%s) %s" % (item.product.name, item.product.size, item.product.color),
                item.stock,
                "<a href='%s' class='btn btn-sm btn-default'><i class='fa fa-pencil-square-o'></i> Ubah</a> <a href='#' onclick='javascript: hapus_stok(%s);' class='btn btn-sm btn-danger'><i class='fa fa-trash'></i> Hapus</a>" % (reverse('update_stock', kwargs = {'pk' : item.id, }), item.id)
            ])
        return json_data

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(Q(name__contains=search) | Q(product__contains=search))

        return qs