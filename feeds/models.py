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


class Entry(models.Model):
    feed = models.ForeignKey('Feed', related_name='entries')
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

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    
    def unread(self,user=None, feed=None):
        if user:
            user_shared_entries = Entry.objects.filter(
                                                       userentry__user_id=user.id,
                                                       userentry__shared=True
                                                       ).values_list('id',flat=True)
            
            unread_count = Entry.objects.filter(
                                                      id in user_shared_entries,
                                                      userentry__user_id=self.user.id,
                                                      userentry__read=True
                                                    ).count()
            return unread_count
        elif feed:
            unread_entries = Entry.objects.filter(feed_id=feed_id)
            unread_count = unread_entries.exclude(
                                                  userentry__user_id=self.user.id,
                                                  userentry__read=True,
                                                 ).count()
            return unread_count 
        else: 
            return None
