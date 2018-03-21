from django.conf.urls import  url
from django.contrib.auth.decorators import login_required
from config.views import home

urlpatterns = [
    url(r'^$', login_required(home), name='config'),
]
