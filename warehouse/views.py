from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic import ListView, DeleteView, CreateView, UpdateView, DetailView
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy, reverse
from django_datatables_view.base_datatable_view import BaseDatatableView
from warehouse.models import Warehouse
from warehouse.forms import WarehouseForm

# Create your views here.
@login_required
def home(request):
    return render(request, 'warehouse/warehouse.html')

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
    # The model we're going to show
    model = Warehouse

    # define the columns that will be returned
    columns = ['name', 'address', 'phone', ]

    # define column names that will be used in sorting
    # order is important and should be same as order of columns
    # displayed by datatables. For non sortable columns use empty
    # value like ''
    order_columns = ['name', 'address', ]

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 500

    #def render_column(self, row, column):
    #    return super(MerkListJson, self).render_column(row, column)

    def prepare_results(self, qs):
        # prepare list with output column data
        # queryset is already paginated here
        json_data = []
        for item in qs:
            json_data.append([
                item.name,
                item.address,
                item.phone,
                "<a href='%s' class='btn btn-sm btn-default'><i class='fa fa-pencil-square-o'></i> Ubah</a> <a href='#' onclick='javascript: hapus_gudang(%s);' class='btn btn-sm btn-danger'><i class='fa fa-trash'></i> Hapus</a>" % (reverse('update_warehouse', kwargs = {'pk' : item.id, }), item.id)
            ])
        return json_data
        
    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(name__contains=search)

        return qs