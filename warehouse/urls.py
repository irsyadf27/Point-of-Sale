from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from warehouse.views import home, WarehouseCreateView, WarehouseEditView, WarehouseDeleteView, WarehouseListJson

urlpatterns = [
    url(r'^$', home, name='warehouse'),
    url(r'^create$', WarehouseCreateView.as_view(), name='create_warehouse'),
    url(r'^update/(?P<pk>[0-9]+)$', WarehouseEditView.as_view(), name='update_warehouse'),
    url(r'^delete/(?P<pk>[0-9]+)$', WarehouseDeleteView.as_view(), name='delete_warehouse'),
    url(r'^data/$', login_required(WarehouseListJson.as_view()), name='warehouse_list_json'),
]
