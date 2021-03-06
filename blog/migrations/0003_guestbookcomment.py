# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blog_entry'),
    ]

    operations = [
        migrations.CreateModel(
            name='GuestbookComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('comment', models.CharField(max_length=2000)),
                ('submitted', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
