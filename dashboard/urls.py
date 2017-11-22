from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from dashboard.views import home

urlpatterns = [
    url(r'^$', home, name='dashboard'),
]
