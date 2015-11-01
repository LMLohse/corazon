from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.views import generic

from .models import Blog, GuestbookComment

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
    recent_blog_posts = Blog.objects.order_by('-submitted')[:15]
    #### without templates:
    # output = ', '.join([p.slug for p in recent_blog_posts])  -> HttpResponse(output)
    context = RequestContext(request, {
        'recent_blog_posts': recent_blog_posts,
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


class GuestbookView(generic.View):
    template_name = 'blog/guestbook.html'

    def get(self, request):
        comments = GuestbookComment.objects.order_by('-submitted')[:100]
        context = RequestContext(request, {
            'comments': comments,
        })
        return render(request, self.template_name, context)

    def post(self, request):
        name = request.POST.get('name')
        comment = request.POST.get('comment')
        if name and comment:
            guestbook_comment = GuestbookComment(name=name, comment=comment)
            guestbook_comment.save()
            return HttpResponseRedirect(reverse('blog:guestbook'))
        else:
            return HttpResponseRedirect(reverse('blog:guestbook'))


class Archive(generic.ArchiveIndexView):
    queryset = Blog.objects.all()
    context_object_name = 'latestposts'
    date_field = "submitted"
    allow_future = True
    template_name = "blog/archive.html"



### guestboll as definition
# def guestbook(request):
#     comments = GuestbookComment.objects.order_by('-submitted')[:100]
#     context = RequestContext(request, {
#         'comments': comments,
#     })
#     return render(request, 'blog/guestbook.html', context)