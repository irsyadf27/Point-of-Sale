from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import logout
from account.views import err_permmision, home, AccountSettingView, AccountCreateView, AccountEditView, AccountDeleteView, AccountListJson

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'account/login.html'}, name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
    url(r'^err_permmision/$', err_permmision, name='err_permmision'),

    url(r'^$', home, name='account'),
    url(r'^create$', AccountCreateView.as_view(), name='create_account'),
    url(r'^update/(?P<pk>[0-9]+)$', AccountEditView.as_view(), name='update_account'),
    url(r'^delete/(?P<pk>[0-9]+)$', AccountDeleteView.as_view(), name='delete_account'),
    url(r'^data/$', login_required(AccountListJson.as_view()), name='account_list_json'),
    url(r'^setting$', login_required(AccountSettingView.as_view()), name='setting_account'),
]
