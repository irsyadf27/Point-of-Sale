from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from returned_product.views import ReturnedProductView, add, remove_cart, set_qty, \
    show_cart, cart_total, testpost, checkout

urlpatterns = [
    url(r'^$', ReturnedProductView.as_view(), name='returned_product'),
    url(r'^add/(?P<pk>[0-9]+)$', add),


    url(r'^set_qty/(?P<pk>[0-9]+)/$', set_qty, name='set_qty_product'),
    url(r'^show_cart/$', show_cart, name='receiving_cart'),
    url(r'^cart_total/$', cart_total, name='receiving_cart'),
    url(r'^remove_cart/(?P<pk>[0-9]+)$', remove_cart, name='remove_cart'),
    url(r'^testpost/$', testpost, name='testpost'),
    url(r'^checkout/$', checkout, name='receiving_checkout'),
]
