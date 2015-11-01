from django.test import TestCase
from .models import Blog, GuestbookComment
from django.utils import timezone
from django.core.urlresolvers import reverse
import datetime


def create_blogpost(entry, slug, days):
    """
    creates a blog post with post and slug published given number of days offset to now
    (negative for post in past, positive for future)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Blog.objects.create(title=slug, author="test", slug=slug, entry=entry, submitted=time, modified=time)


class SimpleTests(TestCase):
    def test_frontpage(self):
        """
        frontpage should always render successful
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_archive(self):
        """
        Empty archive raises 404 error
        """
        response = self.client.get('/blog/archive/')
        self.assertEqual(response.status_code, 404)

    def test_guestbook(self):
        """
        when comment creation works, no "I wonder who will be the first one to write" gets posted
        """
        GuestbookComment.objects.create(name='user', comment='testing')
        response = self.client.get('/guestbook/')
        self.assertNotContains(response, 'I wonder who will be the first one to write')


class BlogTests(TestCase):
    def test_blog(self):
        """
        when blogpost creation works, no "no blog posts" gets posted
        """
        create_blogpost(entry="This is for testing", slug='test_blog', days=0)
        response = self.client.get('/blog/')
        self.assertNotContains(response, 'Still no blog posts here')

    def test_archive_list_display(self):
        """
        TEST CURRENTLY DOESNT WORK AS PLANNED
        auto_now_add overrides, so tests won't work for future, past blospost -> use mock time functions as workaround
        """
        create_blogpost(entry="post3", slug="next_year", days=365)
        create_blogpost(entry="post1", slug="test_this_year", days=0)
        #create_blogpost(entry="post2", slug="last_year", days=-370)
        time = timezone.now() + datetime.timedelta(-365)
        post = Blog(title='manuel', author="test", slug='manuel', entry='really', submitted=time)
        year = datetime.date.today().year
        self.assertEqual(post.submitted.year, year - 1)
        response = self.client.get(reverse('blog:archive'))
        self.assertContains(response, '<p>' + str(year) + '</p>')
        #self.assertContains(response, '<p>' + str(year - 1) + '</p>')
        #self.assertContains(response, '<p>' + str(year + 1) + '</p>')


