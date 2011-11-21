from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns(
    'feedme.feeds.views',
    url(r'^$', 'home', name='home'),
    url(r'^import/', 'import_opml', name='import'),

    # General feed views
    url(r'^feed/(?P<feed_id>\d+)/$', 'feed', name='feed'),
    url(r'^feed/(?P<feed_id>\d+)/all/$', 'feed', kwargs={'unread': False}),
    url(r'^shares/$', 'shares', name='shares'),

    # User feed views
    url(r'^subscribe/(?P<feed_id>\d+)/$', 'subscribe', name='subscribe'),
    url(r'^unsubscribe/(?P<feed_id>\d+)/$', 'unsubscribe', name='unsubscribe'),

    # User entry views
    url(r'^read/(?P<entry_id>\d+)/$', 'read', name='read'),
    url(r'^share/(?P<entry_id>\d+)/$', 'share', name='share'),
    
    url(r'^external_share/$','external_share', name='external_share'),
    url(r'^bookmarklet/(?P<user_id>\d+)/$','bookmarklet', name='bookmarklet')
)
