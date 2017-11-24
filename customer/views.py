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
    model = Customer
    columns = ['name', 'address', 'phone']
    order_columns = ['name', 'address', 'phone']
    max_display_length = 500

    def prepare_results(self, qs):
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