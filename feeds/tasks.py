import time
import datetime
import HTMLParser
import feedparser
from celery.decorators import task
from feedme.feeds.models import Feed, Entry


@task(ignore_result=True)
def refresh_feeds():
    for feed_id in Feed.objects.values_list('id', flat=True):
        refresh_feed.subtask().delay(feed_id)


@task(ignore_result=True)
def refresh_feed(feed_id):
    # Used to unescape html entities in titles
    html_parser = HTMLParser.HTMLParser()

    feed = Feed.objects.get(pk=feed_id)

    parsed = feedparser.parse(feed.uri)
    parsed_feed = parsed.feed

    feed.title = html_parser.unescape(parsed_feed.title)
    feed.save()

    for parsed_entry in parsed.entries:
        uuid = getattr(parsed_entry, 'id', parsed_entry.link)

        try:
            entry = Entry.objects.get(uuid=uuid)
        except Entry.DoesNotExist:
            entry = Entry()
            entry.feed = feed
            entry.uuid = uuid

        entry.link = parsed_entry.link
        entry.title = html_parser.unescape(parsed_entry.title)
        entry.author = getattr(parsed_entry, 'author', None)

        timestamp = time.mktime(parsed_entry.updated_parsed)
        entry.published = datetime.datetime.fromtimestamp(timestamp)

        if hasattr(parsed_entry, 'content'):
            entry.content = parsed_entry.content[0].value
        elif hasattr(parsed_entry, 'summary'):
            entry.content = parsed_entry.summary

        entry.save()
