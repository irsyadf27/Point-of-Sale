from django.conf.urls import include, url
from dashboard.views import home

urlpatterns = [
    url(r'^$', home, name='dashboard'),
]
