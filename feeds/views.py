import xml.etree.ElementTree
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from feedme.feeds.models import Feed, Entry
from feedme.feeds.forms import ImportForm


@login_required
def home(request):
    return render(request, 'feeds/home.html', {
        'feeds': request.user.feeds.all(),
    })


def feed(request, feed_id):
    feed = get_object_or_404(Feed, pk=feed_id)
    if request.method == 'POST':
        feed.refresh()
        return redirect('feed', feed_id=feed.id)
    else:
        return render(request, 'feeds/feed.html', {'feed': feed})


@login_required
def import_opml(request):
    if request.method == 'POST':
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            dom = xml.etree.ElementTree.parse(request.FILES['file'])
            for el in dom.iter('outline'):
                feed = Feed()
                feed.uri = el.attrib['xmlUrl']
                feed.title = el.attrib['title']
                feed.save()
                feed.users.add(request.user)
            return redirect('home')
    else:
        form = ImportForm()
    return render(request, 'feeds/import_opml.html', {'form': form})
