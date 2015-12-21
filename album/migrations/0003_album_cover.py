# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0002_image_thumbnail2'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='cover',
            field=models.FileField(default=None, upload_to=b'images/'),
            preserve_default=True,
        ),
    ]
