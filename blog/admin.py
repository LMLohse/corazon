from django.contrib import admin
from datetime import datetime

from .models import Blog, GuestbookComment


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'slug', 'submitted', 'modified')
    list_filter = ('submitted', 'modified', 'slug')
    search_fields = ('title', 'entry')
admin.site.register(Blog, BlogAdmin)


class GuestbookAdmin(admin.ModelAdmin):
    list_display = ('name', 'submitted')
    list_filter = ('name', 'submitted')
    search_fields = ('name', 'comment')
admin.site.register(GuestbookComment, GuestbookAdmin)

