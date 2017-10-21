from django.conf.urls import url
from . import views
from django.contrib.auth import views as views1
from logdapp.forms import LoginForm

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^name/$', views.get_name, name='get_name'),
    url(r'^login/$', views1.login, {'template_name': 'logdapp/login.html', 'authentication_form': LoginForm}, name='login'),
    url(r'^logout/$', views1.logout, {'next_page': '/logdapp/login'}),
    url(r'^get_grades/$', views.get_grades, name='get_grades'),
    url(r'^update_grades/$', views.update_grades, name='update_grades'),
]
