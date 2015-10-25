from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    entry = models.TextField(editable=True)
    submitted = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.slug


class GuestbookComment(models.Model):
    name = models.CharField(max_length=30)
    comment = models.CharField(max_length=2000)
    submitted = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name