from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from stock.views import home, StockCreateView, StockEditView, StockDeleteView, StockListJson

urlpatterns = [
    url(r'^$', home, name='stock'),
    url(r'^create$', StockCreateView.as_view(), name='create_stock'),
    url(r'^update/(?P<pk>[0-9]+)$', StockEditView.as_view(), name='update_stock'),
    url(r'^delete/(?P<pk>[0-9]+)$', StockDeleteView.as_view(), name='delete_stock'),
    url(r'^data/$', login_required(StockListJson.as_view()), name='stock_list_json'),
]
