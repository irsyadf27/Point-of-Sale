from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic import ListView, DeleteView, CreateView, UpdateView, DetailView
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy, reverse
from django_datatables_view.base_datatable_view import BaseDatatableView
from customer.models import Customer
from customer.forms import CustomerForm

# Create your views here.
@login_required
def home(request):
    return render(request, 'customer/customer.html')

class CustomerCreateView(CreateView):
    form_class = CustomerForm
    model = Customer
    success_url = reverse_lazy('customer')
    template_name = 'customer/create.html'
    #fields = ['name', 'address', 'phone', ]

class CustomerEditView(UpdateView):
    form_class = CustomerForm
    model = Customer
    success_url = reverse_lazy('customer')
    template_name = 'customer/update.html'
    #fields = ['name', 'address', 'phone', ]

class CustomerDeleteView(DeleteView):
    model = Customer
    success_url = reverse_lazy('customer')
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class CustomerListJson(BaseDatatableView):
    # The model we're going to show
    model = Customer

    # define the columns that will be returned
    columns = ['name', 'address', 'phone', ]

    # define column names that will be used in sorting
    # order is important and should be same as order of columns
    # displayed by datatables. For non sortable columns use empty
    # value like ''
    order_columns = ['name', 'address', 'phone', ]

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
                "<a href='%s' class='btn btn-sm btn-default'><i class='fa fa-pencil-square-o'></i> Ubah</a> <a href='#' onclick='javascript: hapus_pelanggan(%s);' class='btn btn-sm btn-danger'><i class='fa fa-trash'></i> Hapus</a>" % (reverse('update_customer', kwargs = {'pk' : item.id, }), item.id)
            ])
        return json_data
        
    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(name__contains=search)

        return qs