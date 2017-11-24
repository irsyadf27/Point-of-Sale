from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from discount.views import home, DiscountCreateView, DiscountEditView, DiscountDeleteView, DiscountListJson

urlpatterns = [
    url(r'^$', home, name='discount'),
    url(r'^create/$', DiscountCreateView.as_view(), name='create_discount'),
    url(r'^update/(?P<pk>[0-9]+)$', DiscountEditView.as_view(), name='update_discount'),
    url(r'^delete/(?P<pk>[0-9]+)$', DiscountDeleteView.as_view(), name='delete_discount'),
    url(r'^data/$', login_required(DiscountListJson.as_view()), name='discount_list_json'),

]
