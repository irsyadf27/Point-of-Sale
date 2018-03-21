from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from customer.views import home, CustomerCreateView, CustomerEditView, CustomerDeleteView, \
    CustomerListJson, list_json

urlpatterns = [
    url(r'^$', home, name='customer'),
    url(r'^create/$', csrf_exempt(CustomerCreateView.as_view()), name='create_customer'),
    url(r'^update/(?P<pk>[0-9]+)$', login_required(CustomerEditView.as_view()), name='update_customer'),
    url(r'^delete/(?P<pk>[0-9]+)$', login_required(CustomerDeleteView.as_view()), name='delete_customer'),
    url(r'^data/$', login_required(CustomerListJson.as_view()), name='customer_list_json'),
    url(r'^list_json/$', list_json, name='customer_json'),
]
