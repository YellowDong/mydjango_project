from django.conf.urls import url
from . import views

urlpatterns = [url(r'^form_test/$', views.register_views),
               url(r'^form_handle/$', views.register_handle),
               ]