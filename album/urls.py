from django.conf.urls import patterns, url
from album import views
from django.views.generic.edit import CreateView

urlpatterns = patterns('',

        url(r'^$', views.home, name='home'),
        url(r'^album/(?P<pk>\d+)/$', views.album_view,name='album_view'),
        url(r'^image/(?P<pk>\d+)/$', views.image_view,name='image_view'),
        url(r'^upload/$', views.UploadView.as_view(), name='upload'),
        url(r'^list/', views.main, name='main'),
)
