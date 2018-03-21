from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from report.views import home, get_json, export_report_xls

urlpatterns = [
    url(r'^$', home, name='report'),
    url(r'^get_json/$', get_json, name='report_get_json'),
    url(r'^export/$', export_report_xls, name='export_report_xls'),
]
