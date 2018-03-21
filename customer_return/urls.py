from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from customer_return.views import home, get_invoice, show_cart, cart_total, \
    testpost, checkout, set_qty

urlpatterns = [
    url(r'^$', home, name='customer_return'),
    url(r'^get_invoice/(?P<invoice_number>[a-zA-Z\-0-9]+)$', get_invoice, name='get_invoice_customer_return'),


    url(r'^set_qty/(?P<pk>[0-9]+)/$', set_qty, name='set_qty_product_customer_return'),
    url(r'^show_cart/$', show_cart, name='receiving_cart_customer_return'),
    url(r'^cart_total/$', cart_total, name='receiving_cart_customer_return'),
    url(r'^testpost/$', testpost, name='testpost_customer_return'),
    url(r'^checkout/$', checkout, name='receiving_checkout_customer_return'),
]