from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from report.views import home

urlpatterns = [
    url(r'^$', home, name='report'),
]
