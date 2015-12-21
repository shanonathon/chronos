# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0003_album_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='cover',
            field=models.FileField(default=None, null=True, upload_to=b'images/'),
            preserve_default=True,
        ),
    ]
