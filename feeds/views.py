import feedparser
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render
from feedme.feeds.models import Feed, Entry


def feed(request, feed_id):
    feed = get_object_or_404(Feed, pk=feed_id)
    return render(request, 'feeds/feed.html', {'feed': feed})


@require_POST
def refresh(request, feed_id):
    feed = get_object_or_404(Feed, pk=feed_id)
    parsed = feedparser.parse(feed.uri)

    parsed_feed = parsed['feed']
    feed.title = parsed_feed['title']
    feed.save()

    for parsed_entry in parsed['entries']:
        entry = Entry()
        entry.feed = feed
        entry.author = parsed_entry['author']
        entry.title = parsed_entry['title']
        entry.content = parsed_entry['summary']
        entry.save()

    return redirect('feed', feed_id=feed.id)
