import time, datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.mail import send_mail, BadHeaderError
from django.template import RequestContext, loader
from django.views import generic
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from .models import Blog, GuestbookComment
from .forms import GuestbookForm, EmailForm
from .functions import caching_functions

from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.


def frontpage(request):
    # return HttpResponse('test frontpage')
    return render(request, 'blog/frontpage.html')


def blog(request):
    #recent_blog_posts = Blog.objects.order_by('-submitted')[:5]
    recent_blog_posts = caching_functions.blog_cache()[:5]
    queried = round(time.time() - caching_functions.get_query_time())
    last_queried = "Queried %s seconds ago" % str(queried)
    context = RequestContext(request, {
        'recent_blog_posts': recent_blog_posts,
        'last_queried': last_queried,
    })
    return render(request, 'blog/blog.html', context)


class BlogRSSFeed(Feed):
    title = 'LMLohse latest posts'
    link = '/blog/'
    description = 'You are the best ever.'

    def items(self):
        return caching_functions.blog_cache()[:12]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.entry

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse('blog:slug', args=[item.slug])

    def item_pubdate(self, item):
        return item.submitted


class BlogAtem1Feed(BlogRSSFeed):
    feed_type = Atom1Feed
    subtitle = BlogRSSFeed.description
    author_name = 'Lukas M. Lohse'

    def item_updateddate(self, item):
        return item.modified


def projects(request):
    return render(request, 'blog/projects.html')


def development(request):
    return render(request, 'blog/development.html')


class SlugView(generic.DetailView):
    template_name = 'blog/slug.html'
    model = Blog
    #### the same without generic view
    # def slugview(request, slug):
    #     blog_post = get_object_or_404(Blog, slug=slug)
    #     return render(request, 'blog/slug.html', {'blog_post': blog_post})


# EMAIL-VERSION
# def me(request):
#     has_submit_error = False
#     if request.method == "POST":
#         form = EmailForm(request.POST)
#         if form.is_valid():
#             subject = form.cleaned_data['subject']
#             message = form.cleaned_data['content']
#             sender = form.cleaned_data['sender_email']
#             receiver = 'lukas.lohse22@gmail.com'
#             try:
#                 send_mail(subject, message, sender, [receiver], fail_silently=False)
#             except BadHeaderError:
#                 return HttpResponse('Invalid header')
#             return HttpResponseRedirect('/')
#         else:
#             return HttpResponseRedirect('/blog')
#             #has_submit_error = True
#             # do an ajax ??
#     else:
#         form = EmailForm()
#     context = RequestContext(request, {
#         'form': form,
#         'has_error': has_submit_error,
#     })
#     return render(request, 'blog/me.html', context)

class MeView(generic.TemplateView):
    template_name = 'blog/me.html'


def guestbook(request):
    has_submit_error = False
    if request.method == 'POST':
        form = GuestbookForm(request.POST)
        if form.is_valid():
            guestbook_comment = GuestbookComment(name=form.cleaned_data['name'], comment=form.cleaned_data['comment'])
            guestbook_comment.save()
            caching_functions.guestbook_cache(update=True)
            return HttpResponseRedirect(reverse('blog:guestbook'))
        else:
            has_submit_error = True
    else:
        form = GuestbookForm()
    #comments = GuestbookComment.objects.order_by('-submitted')[:30]
    comments = caching_functions.guestbook_cache()[:30]
    context = RequestContext(request, {
        'form': form,
        'comments': comments,
        'has_error': has_submit_error,
    })
    return render(request, 'blog/guestbook.html', context)


class Archive(generic.ArchiveIndexView):
    #queryset = Blog.objects.all()
    queryset = caching_functions.blog_cache()
    context_object_name = 'latestposts'
    date_field = "submitted"
    allow_future = True
    template_name = "blog/archive.html"


