from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^$', views.upTime, name='index'),
    url(r'upT/$', views.upTime, name='upTime'),
    url(r'downT/$', views.downTime, name='downTime'),
    url(r'upU/$', views.upU, name='upU'),
    url(r'downU/$', views.downU, name='downU'),
    ]