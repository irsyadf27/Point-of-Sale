from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from product.views import home, qrcode, list_json, \
    ProductDetailView, ProductCreateView, ProductEditView, \
    ProductDeleteView, ProductListJson, IncomeProductView, \
    MappingListJson

urlpatterns = [
    url(r'^$', home, name='product'),
    url(r'^create/$', ProductCreateView.as_view(), name='create_product'),
    url(r'^update/(?P<pk>[0-9]+)$', ProductEditView.as_view(), name='update_product'),
    url(r'^delete/(?P<pk>[0-9]+)$', ProductDeleteView.as_view(), name='delete_product'),
    url(r'^data/$', login_required(ProductListJson.as_view()), name='product_list_json'),
    url(r'^detail/(?P<pk>[0-9]+)$', ProductDetailView.as_view(), name='detail_product'),
    url(r'^qrcode/(?P<pk>[0-9]+)$', qrcode, name='qrcode_product'),


    url(r'^mapping/(?P<pk>[0-9]+)/$', login_required(MappingListJson.as_view()), name='mapping_product_list_json'),
    url(r'^list_json/$', list_json, name='product_json'),
    url(r'^income/$', IncomeProductView.as_view(), name='income_product'),
]
