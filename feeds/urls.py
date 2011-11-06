from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns(
    'feedme.feeds.views',
    url(r'^$', 'home', name='home'),
    url(r'^import/', 'import_opml', name='import'),
    url(r'^subscribe/(?P<feed_id>\d+)/$', 'subscribe', name='subscribe'),
    url(r'^feed/(?P<feed_id>\d+)/$', 'feed', name='feed'),
    url(r'^feed/(?P<feed_id>\d+)/all/$', 'feed', kwargs={'unread': False}),
    url(r'^unsubscribe/(?P<feed_id>\d+)/$', 'unsubscribe', name='unsubscribe'),
)
