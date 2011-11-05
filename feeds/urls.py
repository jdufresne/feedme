from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns(
    'feedme.feeds.views',
    url(r'^$', 'home', name='home'),
    url(r'^import/', 'import_opml', name='import'),
    url(r'^feed/(?P<feed_id>\d+)/$', 'feed', name='feed'),
)
