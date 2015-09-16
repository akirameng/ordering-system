# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dish',
            old_name='like',
            new_name='liked',
        ),
        migrations.RenameField(
            model_name='dish',
            old_name='unlike',
            new_name='unliked',
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='category',
            field=models.CharField(default=b'cns', max_length=10, verbose_name=b'Food Type', choices=[(b'ff', b'FastFood'), (b'cns', b'Chinese'), (b'jpf', b'Japanese'), (b'wst', b'Western')]),
        ),
    ]
