import time

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.views import generic

from .models import Blog, GuestbookComment
from .forms import GuestbookForm
from .functions import caching_functions

from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
# /         - Homepage (static links for now)
# /blog     - 10 most recent blog posts
#   /blog/slug      - Permalinks
# /projects - static list page
# /vita     - static list page
# /contact  - static links page
# /progress - static list page


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


class MeView(generic.TemplateView):
    template_name = 'blog/me.html'
    # this is equal to:
    # def me(request):
    #     return render(request, 'blog/me.html')


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


