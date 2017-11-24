from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from merk.views import home, MerkCreateView, MerkEditView, MerkDeleteView, MerkListJson

urlpatterns = [
    url(r'^$', home, name='merk'),
    url(r'^create/$', MerkCreateView.as_view(), name='create_merk'),
    url(r'^update/(?P<pk>[0-9]+)$', MerkEditView.as_view(), name='update_merk'),
    url(r'^delete/(?P<pk>[0-9]+)$', MerkDeleteView.as_view(), name='delete_merk'),
    url(r'^data/$', login_required(MerkListJson.as_view()), name='merk_list_json'),

]
