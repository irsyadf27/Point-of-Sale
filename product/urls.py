from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from product.views import home, ProductCreateView, ProductEditView, ProductDeleteView, ProductListJson

urlpatterns = [
    url(r'^$', home, name='product'),
    url(r'^create$', ProductCreateView.as_view(), name='create_product'),
    url(r'^update/(?P<pk>[0-9]+)$', ProductEditView.as_view(), name='update_product'),
    url(r'^delete/(?P<pk>[0-9]+)$', ProductDeleteView.as_view(), name='delete_product'),
    url(r'^data/$', login_required(ProductListJson.as_view()), name='product_list_json'),
]
