from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    None,
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^accounts/', include('registration.urls')),
    url(r'^', include('feedme.feeds.urls')),
)
