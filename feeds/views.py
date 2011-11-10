from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from feedme.ajax import json_response
from feedme.feeds.models import Feed, Entry, UserEntry
from feedme.feeds.forms import ImportForm
from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import datetime

def feed(request, feed_id, unread=True):
    feed = get_object_or_404(Feed, pk=feed_id)
    if request.method == 'POST':
        feed.refresh()
        return redirect('feed', feed_id=feed.id)
    else:
        entries = feed.entries
        if request.user.is_authenticated():
            if unread:
                entries = entries.exclude(userentry__user=request.user,
                                          userentry__read=True)
            subscribed = request.user.feeds.filter(pk=feed.id).exists()
        else:
            entries = entries.all()
            subscribed = None

        return render(request, 'feeds/feed.html', {
            'feed': feed,
            'entries': entries,
            'subscribed': subscribed,
        })


def shares(request, unred=True):
    entries = Entry.objects.filter(userentry__shared=True)
    if request.user.is_authenticated():
        entries = entries.exclude(userentry__user=request.user)
    return render(request, 'feeds/shares.html', {'entries': entries})


def home(request):
    if request.user.is_authenticated():
        user = request.user
    else: 
        user = 'admin' 
    bm_url = "javascript:(function(){if(typeof%20jQuery=='undefined'){var%20jQ=document.createElement('script');jQ.type='text/javascript';jQ.onload=runthis;jQ.src='http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js';document.body.appendChild(jQ);}else{runthis();}function%20runthis(){var%20title=document.title;var%20url=document.URL;var%20comment=prompt('Share%20with%20comment:');$.post('http://127.0.0.1:8000/external_share/',{title:title,comment:comment,url:url,user:"+ user.username +",},function(data){alert(data);});}})()"  
    return render(request, 'feeds/home.html')


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
    user_entry, created = UserEntry.objects.get_or_create(user=request.user,
                                                          entry=entry)
    user_entry.read = True
    user_entry.save()
    if request.is_ajax():
        return json_response({'success': True})
    return redirect('feed', feed_id=entry.feed.id)


@login_required
@require_POST
def share(request, entry_id):
    entry = get_object_or_404(Entry, pk=entry_id)
    user_entry, created = UserEntry.objects.get_or_create(user=request.user,
                                                          entry=entry)
    user_entry.shared = True
    user_entry.save()
    if request.is_ajax():
        return json_response({'success': True})
    return redirect('feed', feed_id=entry.feed.id)

@csrf_exempt
def external_share(request):
    if request.method == 'POST':
        user = User.objects.get(username__exact=request.POST['user'])
        url = request.POST['url']
        comment = request.POST['comment']
        title = request.POST['title']
        entries = Entry.objects.filter(link=url)
        if not entries:
            entry = Entry()
            entry.content = comment
            entry.uuid = url
            entry.link = url
            entry.title = title
            entry.feed = None
            entry.published = datetime.date.today()
            entry.save()
            print "entry saved"
            user_entry = UserEntry()
            user_entry.user = user
            print "new userentry"
        else :
            print "already"
            entry = entries[0]
            try:
                user_entry = UserEntry.objects.get(user=user,entry=entry)
            except UserEntry.DoesNotExist:
                user_entry = UserEntry()
        print "a"
        user_entry.user = user
        print "b"
        user_entry.entry = entry
        print "c"
        user_entry.shared = True
        user_entry.read = True
        user_entry.save()
        print "saved"
        return HttpResponse("saved")
    else:
        return HttpResponse(status=404)

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
