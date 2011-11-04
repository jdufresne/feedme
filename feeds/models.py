from django.db import models


class Feed(models.Model):
    uri = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.uri
        super(Feed, self).save(*args, **kwargs)


class Article(models.Model):
    feed = models.ForeignKey('Feed')
