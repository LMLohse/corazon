import logging
import time

from django.db.models.signals import post_save, post_delete
from django.core.cache import cache
from django.dispatch import receiver
from blog.models import Blog, GuestbookComment

DBCURRY_MESSAGE_BLOG = 'DB Curry in Blog model'
DBCURRY_MESSAGE_GUESTBOOK = 'DB Curry in Guestbook model'
BLOG_KEY = 'blog'
GUESTBOOK_KEY = 'guestbook'


@receiver(post_save, sender=Blog)
def update_blog_post_save(sender, **kwargs):
    logging.warning(DBCURRY_MESSAGE_BLOG)
    blogposts = Blog.objects.order_by('-submitted')
    cache.set(BLOG_KEY, blogposts)
    cache.set('time', time.time())


@receiver(post_delete, sender=Blog)
def update_blog_post_delete(sender, **kwargs):
    logging.warning(DBCURRY_MESSAGE_BLOG)
    blogposts = Blog.objects.order_by('-submitted')
    cache.set(BLOG_KEY, blogposts)
    cache.set('time', time.time())


def clear_guestbook_cache(sender, **kwargs):
    cache.delete(GUESTBOOK_KEY)

# Set up signals
post_save.connect(clear_guestbook_cache, sender=GuestbookComment)
post_delete.connect(clear_guestbook_cache, sender=GuestbookComment)


def blog_cache():
    blogposts = cache.get(BLOG_KEY)
    if blogposts is None:
        logging.warning(DBCURRY_MESSAGE_BLOG)
        blogposts = Blog.objects.order_by('-submitted')
        cache.set(BLOG_KEY, blogposts)
        cache.set('time', time.time())
    return blogposts


def guestbook_cache(update=False):
    comments = cache.get(GUESTBOOK_KEY)
    if comments is None or update:
        logging.warning(DBCURRY_MESSAGE_GUESTBOOK)
        comments = GuestbookComment.objects.order_by('-submitted')
        cache.set(GUESTBOOK_KEY, comments)
    return comments


def get_query_time():
    return cache.get('time')