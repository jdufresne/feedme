from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render
from feedme.feeds.models import Feed


def feed(request, feed_id):
    feed = get_object_or_404(Feed, pk=feed_id)
    return render(request, 'feeds/feed.html', {'feed': feed})


@require_POST
def refresh(request, feed_id):
    feed = get_object_or_404(Feed, pk=feed_id)
    return redirect('feed', feed_id=feed.id)
