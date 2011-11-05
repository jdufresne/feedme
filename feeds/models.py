import feedparser
from django.db import models
from django.contrib.auth.models import User


class Feed(models.Model):
    uri = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255, blank=True)
    users = models.ManyToManyField(User, related_name='feeds')

    def __unicode__(self):
        return self.title

    def clean(self):
        if not self.title:
            self.title = self.uri
        super(Feed, self).clean()

    def refresh(self):
        parsed = feedparser.parse(self.uri)

        parsed_feed = parsed.feed
        self.title = parsed_feed.title
        self.save()

        for parsed_entry in parsed.entries:
            try:
                entry = Entry.objects.get(uuid=parsed_entry.id)
            except Entry.DoesNotExist:
                entry = Entry()
	            entry.feed = self

            entry.uuid = parsed_entry.id
            entry.link = parsed_entry.link
            entry.title = parsed_entry.title
            entry.author = parsed_entry.author

            if hasattr(parsed_entry, 'content'):
                entry.content = parsed_entry.content[0].value
            else:
                entry.content = parsed_entry.summary

            entry.save()


class Entry(models.Model):
    feed = models.ForeignKey('Feed', related_name='entries')
    uuid = models.CharField(max_length=255, unique=True)
    link = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    content = models.TextField()

    def __unicode__(self):
        return self.title
