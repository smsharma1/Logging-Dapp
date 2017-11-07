from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^grantpermissions/$', views.grant_permissions, name='grant_permissions'),
    url(r'^get_grades/$', views.get_grades, name='get_grades'),
    url(r'^update_grades/$', views.update_grades, name='update_grades'),
    url(r'^breach/$', views.blockchain_breach, name='breach'),
]
