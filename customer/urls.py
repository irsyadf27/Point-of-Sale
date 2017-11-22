from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from customer.views import home, CustomerCreateView, CustomerEditView, CustomerDeleteView, CustomerListJson

urlpatterns = [
    url(r'^$', home, name='customer'),
    url(r'^create$', CustomerCreateView.as_view(), name='create_customer'),
    url(r'^update/(?P<pk>[0-9]+)$', CustomerEditView.as_view(), name='update_customer'),
    url(r'^delete/(?P<pk>[0-9]+)$', CustomerDeleteView.as_view(), name='delete_customer'),
    url(r'^data/$', login_required(CustomerListJson.as_view()), name='customer_list_json'),
]
