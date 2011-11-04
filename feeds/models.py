from django.db import models


class Feed(models.Model):
    uri = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True)

    def clean(self):
        if not self.title:
            self.title = self.uri
        super(Feed, self).clean()

    def __unicode__(self):
        return self.title


class Entry(models.Model):
    feed = models.ForeignKey('Feed', related_name='entries')
    author = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    content = models.TextField()
