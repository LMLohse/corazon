from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.frontpage, name="frontpage"),
    url(r'^blog/$', views.blog, name="blog"),
    url(r'^blog/archive/$', views.Archive.as_view(), name='archive'),
    url(r'^blog/(?P<slug>[-_\w]+)/$', views.SlugView.as_view(), name="slug"),
    url(r'^projects/$', views.projects, name="projects"),
    url(r'^development/$', views.development, name="development"),
    url(r'^me/$', views.MeView.as_view(), name="me"),
    url(r'^guestbook/$', views.GuestbookView.as_view(), name='guestbook'),
]
