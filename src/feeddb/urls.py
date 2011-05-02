from django.conf.urls.defaults import *
from django.conf import settings
from views import * 

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^feeddb/', include('feeddb.foo.urls')),

    (r'^static/(?P<path>.*)$', 
     'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    (r'^uploads/(?P<path>.*)$', 
     'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^admin/', include(admin.site.urls)),
    #(r'^feed/', include(admin.site.urls)),
    (r'^$', 'feeddb.feed.views.index'),
    #(r'^$', include('feeddb.feed.urls')),
    (r'^explorer/', include('feeddb.explorer.urls')),
    (r'^about', 'feeddb.feed.views.about'),
    (r'^welcome', 'feeddb.feed.views.welcome'), 
    (r'^login$', login_view),
    (r'^logout$', logout_view),
)
