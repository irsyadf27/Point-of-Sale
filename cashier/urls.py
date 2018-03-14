from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from cashier.views import home, set_qty, add, show_cart, cart_total, remove_cart, \
    testpost, mapping, checkout, InvoiceView

urlpatterns = [
    url(r'^$', home, name='cashier'),

    url(r'^add/$', add, name='add_cart_cashier'),
    url(r'^set_qty/(?P<pk>[0-9]+)/$', set_qty, name='set_qty_cashier'),
    url(r'^show_cart/$', show_cart, name='cashier_cart'),
    url(r'^cart_total/$', cart_total, name='cashier_cart_total'),
    url(r'^remove_cart/(?P<pk>[0-9]+)$', remove_cart, name='remove_cart_cashier'),
    url(r'^testpost/$', testpost, name='testpost_cashier'),
    url(r'^mapping/$', mapping, name='mapping_cashier'),
    url(r'^checkout/$', checkout, name='checkout_cashier'),

    url(r'^invoice/(?P<invoice_number>[a-zA-Z\-0-9]+)$', InvoiceView.as_view(), name='invoice_detail'),
]
