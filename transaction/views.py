from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy, reverse
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.views.generic import DetailView
from cashier.models import Invoice

# Create your views here.
@login_required
def home(request):
    return render(request, 'transaction/transaction.html')

class TransactionDetailView(DetailView):
    model = Invoice
    template_name = 'transaction/detail.html'
    slug_field = 'invoice_number'
    slug_url_kwarg = 'invoice_number'
    query_pk_and_slug = True

class TransactionListJson(BaseDatatableView):
    model = Invoice
    columns = ['invoice_number', 'customer_name', 'created_at', 'qty', 'total']
    order_columns = ['invoice_number', 'customer_name', 'created_at', 'qty', 'total']
    max_display_length = 500

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.invoice_number,
                item.customer.name,
                item.created_at,
                item.qty,
                item.total,
                "<a href='%s' class='btn btn-sm btn-default'><i class='fa fa-pencil-square-o'></i> Detail</a>" % (reverse('detail_transaction', kwargs = {'pk' : item.id, }))
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