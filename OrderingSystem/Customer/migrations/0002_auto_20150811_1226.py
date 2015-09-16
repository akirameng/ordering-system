# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='restaurant',
            field=models.ForeignKey(related_name='restaurant', to='business.Restaurant'),
        ),
        migrations.AlterField(
            model_name='order',
            name='time',
            field=models.DateTimeField(),
        ),
    ]
