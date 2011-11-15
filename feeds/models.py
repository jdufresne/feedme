from django.db import models
from django.contrib.auth.models import User


class Feed(models.Model):
    uri = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255, blank=True)
    users = models.ManyToManyField(User, related_name='feeds')

    class Meta:
        ordering = ('title',)

    def __unicode__(self):
        return self.title

    def clean(self):
        if not self.title:
            self.title = self.uri
        super(Feed, self).clean()

    def refresh(self):
        # Used to unescape html entities in titles
        html_parser = HTMLParser.HTMLParser()

        parsed = feedparser.parse(self.uri)
        if parsed['bozo']:
            return
        parsed_feed = parsed.feed
        #try:
        self.title = html_parser.unescape(parsed_feed.title)
        #except:
        #    self.title = parsed_feed.title
        self.save()

        for parsed_entry in parsed.entries:
            uuid = getattr(parsed_entry, 'id', parsed_entry.link)

            try:
                entry = Entry.objects.get(uuid=uuid)
            except Entry.DoesNotExist:
                entry = Entry()
                entry.feed = self
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



class Entry(models.Model):
    feed = models.ForeignKey('Feed', related_name='entries', null=True, blank=True)
    uuid = models.CharField(max_length=255, unique=True)
    link = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, null=True, blank=True)
    published = models.DateTimeField()
    content = models.TextField(null=True, blank=True)
    users = models.ManyToManyField(User,
                                   related_name='entries',
                                   through='UserEntry')

    class Meta:
        ordering = ('-published',)

    def __unicode__(self):
        return self.title


class UserEntry(models.Model):
    user = models.ForeignKey(User)
    entry = models.ForeignKey('Entry')
    read = models.BooleanField(default=False)
    bookmarked = models.BooleanField(default=False)
    shared = models.BooleanField(default=False)
