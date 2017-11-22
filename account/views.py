from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic import ListView, DeleteView, CreateView, UpdateView, DetailView
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy, reverse
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.contrib.auth.models import User
from account.forms import AccountForm

# Create your views here.
@login_required
def err_permmision(request):
    return render(request, 'account/error_permmision.html')

@login_required
def home(request):
    if not request.user.is_superuser:
        return redirect(reverse_lazy('err_permmision'))
    return render(request, 'account/account.html')

class AccountCreateView(CreateView):
    form_class = AccountForm
    model = User
    success_url = reverse_lazy('account')
    template_name = 'account/create.html'
    #fields = ['first_name', 'last_name', 'username', 'email', 'is_superuser', 'password', ]

class AccountEditView(UpdateView):
    form_class = AccountForm
    model = User
    success_url = reverse_lazy('account')
    template_name = 'account/update.html'
    #fields = ['first_name', 'last_name', 'username', 'email', 'is_superuser', 'password', ]

class AccountDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('account')
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class AccountListJson(BaseDatatableView):
    # The model we're going to show
    model = User

    # define the columns that will be returned
    columns = ['first_name', 'last_name', 'username', 'email', 'is_superuser', ]

    # define column names that will be used in sorting
    # order is important and should be same as order of columns
    # displayed by datatables. For non sortable columns use empty
    # value like ''
    order_columns = ['first_name', 'last_name', 'username', 'email', 'is_superuser', ]

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
                item.first_name,
                item.last_name,
                item.username,
                item.email,
                '<span class="label label-success"><i class="fa fa-check"></i></span>' if item.is_superuser else '<span class="label label-danger"><i class="fa fa-close"></i></span>',
                "<a href='%s' class='btn btn-sm btn-default'><i class='fa fa-pencil-square-o'></i> Ubah</a> <a href='#' onclick='javascript: hapus_pengguna(%s);' class='btn btn-sm btn-danger'><i class='fa fa-trash'></i> Hapus</a>" % (reverse('update_account', kwargs = {'pk' : item.id, }), item.id)
            ])
        return json_data
        
    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(Q(first_name__contains=search) | 
                Q(last_name__contains=search) | 
                Q(username__contains=search) |
                Q(email__contains=search)
                )

        return qs