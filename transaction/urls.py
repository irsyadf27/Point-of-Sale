from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from transaction.views import home, TransactionListJson, TransactionDetailView

urlpatterns = [
    url(r'^$', home, name='transaction'),
    url(r'^data/$', login_required(TransactionListJson.as_view()), name='transaction_list_json'),
    url(r'^detail/(?P<invoice_number>[a-zA-Z\-0-9]+)$', login_required(TransactionDetailView.as_view()), name='detail_transaction'),
]
