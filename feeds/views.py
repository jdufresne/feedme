from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from feedme.feeds.models import Feed, Entry
from feedme.feeds.forms import ImportForm


def feed(request, feed_id, unread=True):
    feed = get_object_or_404(Feed, pk=feed_id)
    if request.method == 'POST':
        feed.refresh()
        return redirect('feed', feed_id=feed.id)
    else:
        entries = feed.entries.all()
        if request.user.is_authenticated():
            subscribed = request.user.feeds.filter(pk=feed.id).exists()
            if unread:
                entries = entries.exclude(pk__in=request.user.entries.all())
        else:
            subscribed = None

        return render(request, 'feeds/feed.html', {
            'feed': feed,
            'entries': entries,
            'subscribed': subscribed,
        })


@login_required
def home(request):
    return render(request, 'feeds/home.html', {
        'feeds': request.user.feeds.all(),
    })


@login_required
@require_POST
def subscribe(request, feed_id):
    feed = get_object_or_404(Feed, pk=feed_id)
    request.user.feeds.add(feed)
    return redirect('feed', feed_id=feed.id)


@login_required
@require_POST
def unsubscribe(request, feed_id):
    feed = get_object_or_404(Feed, pk=feed_id)
    request.user.feeds.remove(feed)
    return redirect('feed', feed_id=feed.id)


@login_required
@require_POST
def read(request, entry_id):
    entry = get_object_or_404(Entry, pk=entry_id)
    request.user.entries.add(entry)
    return redirect('feed', feed_id=entry.feed.id)


@login_required
def import_opml(request):
    if request.method == 'POST':
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.cleaned_data['opml']
            for el in doc.iterfind('//outline[@type="rss"]'):
                try:
                    feed = Feed.objects.get(uri=el.attrib['xmlUrl'])
                except Feed.DoesNotExist:
                    feed = Feed()
                    feed.uri = el.attrib['xmlUrl']
                    feed.title = el.attrib['text']
                    feed.save()
                request.user.feeds.add(feed)
            return redirect('home')
    else:
        form = ImportForm()
    return render(request, 'feeds/import_opml.html', {'form': form})
