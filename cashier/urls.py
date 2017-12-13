from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from cashier.views import home, set_qty, add, show_cart, cart_total, remove_cart

urlpatterns = [
    url(r'^$', home, name='cashier'),

    url(r'^add/$', add, name='add_cart_cashier'),
    url(r'^set_qty/(?P<pk>[0-9]+)/$', set_qty, name='set_qty_cashier'),
    url(r'^show_cart/$', show_cart, name='cashier_cart'),
    url(r'^cart_total/$', cart_total, name='cashier_cart_total'),
    url(r'^remove_cart/(?P<pk>[0-9]+)$', remove_cart, name='remove_cart_cashier'),
]
