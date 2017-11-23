from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from warehouse.views import home, WarehouseDetailView, WarehouseCreateView, \
    WarehouseEditView, WarehouseDeleteView, WarehouseListJson, \
    WarehouseProductListJson

urlpatterns = [
    url(r'^$', home, name='warehouse'),
    url(r'^detail/(?P<pk>[0-9]+)$', WarehouseDetailView.as_view(), name='detail_warehouse'),
    url(r'^create$', WarehouseCreateView.as_view(), name='create_warehouse'),
    url(r'^update/(?P<pk>[0-9]+)$', WarehouseEditView.as_view(), name='update_warehouse'),
    url(r'^delete/(?P<pk>[0-9]+)$', WarehouseDeleteView.as_view(), name='delete_warehouse'),
    url(r'^data/$', login_required(WarehouseListJson.as_view()), name='warehouse_list_json'),
    url(r'^product/(?P<pk>[0-9]+)/$', login_required(WarehouseProductListJson.as_view()), name='warehouse_product_list_json'),
]
