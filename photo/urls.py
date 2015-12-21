from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

#from polls import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tiberius.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('album.urls', namespace="album")),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
                                {'next_page': '/login/'})

)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))

    
