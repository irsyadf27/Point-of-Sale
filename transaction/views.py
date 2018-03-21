from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy, reverse
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.views.generic import DetailView
from django.db.models import Q
from cashier.models import Invoice
from datetime import datetime

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
    columns = ['invoice_number', 'customer__name', 'created_at', 'qty', 'total']
    order_columns = ['invoice_number', 'customer__name', 'created_at', 'qty', 'total']
    max_display_length = 500

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.invoice_number,
                item.customer.name,
                datetime.strftime(item.created_at, "%a, %d %b %Y %H:%M"),
                item.qty,
                item.total,
                "<a href='%s' class='btn btn-sm btn-primary'><i class='fa fa-credit-card'></i> Detail</a>" % (reverse('detail_transaction', kwargs = {'invoice_number' : item.invoice_number, }))
            ])
        return json_data
        
    def filter_queryset(self, qs):
        start_date = self.request.GET.get(u'start_date', '2018-03-10') + " 00:00:00"
        end_date = self.request.GET.get(u'end_date', '2018-03-16') + " 23:59:59"
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(Q(created_at__range=[start_date,end_date]) & (Q(invoice_number__contains=search) | Q(customer__name__contains=search))).order_by('-created_at')
        else:
            qs = qs.filter(created_at__range=[start_date,end_date]).order_by('-created_at')
        return qs