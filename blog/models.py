from django.db import models
from django.core.urlresolvers import reverse


class Blog(models.Model):
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    entry = models.TextField(editable=True)
    submitted = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('archive', kwargs={'pk': self.pk})


class GuestbookComment(models.Model):
    name = models.CharField(max_length=30)
    comment = models.CharField(max_length=2000)
    submitted = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name