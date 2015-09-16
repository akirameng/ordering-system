# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment_R',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('time', models.DateTimeField()),
                ('rating', models.FloatField(validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(5.0)])),
                ('buyer', models.ForeignKey(related_name='comment_r', to=settings.AUTH_USER_MODEL)),
                ('restaurant', models.ForeignKey(to='business.Restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.TimeField()),
                ('location', models.CharField(max_length=200)),
                ('delivery_type', models.IntegerField()),
                ('total_price', models.DecimalField(max_digits=6, decimal_places=2)),
                ('discount', models.FloatField()),
                ('paid', models.BooleanField(default=False)),
                ('status', models.CharField(default=b'prog', max_length=10, choices=[(b'can', b'Cancelled'), (b'prog', b'In Progress'), (b'fin', b'Complete')])),
                ('buyer', models.ForeignKey(related_name='order', to=settings.AUTH_USER_MODEL)),
                ('restaurant', models.ForeignKey(to='business.Restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('Dish', models.ForeignKey(to='business.Dish')),
                ('Order', models.ForeignKey(related_name='orderitem', to='Customer.Order')),
                ('restaurant', models.ForeignKey(to='business.Restaurant')),
            ],
        ),
    ]
