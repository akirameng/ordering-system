# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=20)),
                ('zipcode', models.CharField(max_length=10)),
                ('latitude', models.FloatField(null=True, blank=True)),
                ('longitude', models.FloatField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('price', models.FloatField()),
                ('image', models.FileField(null=True, upload_to=b'dishes/%Y/%m/%d', blank=True)),
                ('like', models.IntegerField(default=0)),
                ('unlike', models.IntegerField(default=0)),
                ('description', models.TextField(null=True, blank=True)),
                ('dishcategory', models.CharField(default=b'ent', max_length=10, verbose_name=b'Dish Type', choices=[(b'ent', b'Entries'), (b'mai', b'Main'), (b'des', b'Dessert'), (b'drk', b'Drinks')])),
            ],
        ),
        migrations.CreateModel(
            name='DishComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField()),
                ('dish', models.ForeignKey(to='business.Dish')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name=b'Restaurant Name')),
                ('msg', models.TextField(null=True, verbose_name=b'Description', blank=True)),
                ('image', models.FileField(null=True, upload_to=b'restaurant/%Y/%m/%d', blank=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name=b'Business Phone', validators=[django.core.validators.RegexValidator(regex=b'^[+|\\d][0-9() -]*\\d$', message=b'Please enter a correct phone number.')])),
                ('Provide_Delivery', models.BooleanField(default=False)),
                ('Children_Friendly', models.BooleanField(default=False)),
                ('Wifi', models.BooleanField(default=False)),
                ('Vegan', models.BooleanField(default=False)),
                ('Gluten_Free', models.BooleanField(default=False)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('lastAccessAt', models.DateTimeField(auto_now=True)),
                ('category', models.CharField(default=b'cns', max_length=10, verbose_name=b'Food Type', choices=[(b'asa', b'Asian'), (b'ff', b'FastFood'), (b'cns', b'Chinese'), (b'jpf', b'Japanese'), (b'wst', b'Western')])),
                ('opentime', models.CharField(default=b'08:00', max_length=10, verbose_name=b'Open Time', choices=[(b'06:00', b'06:00'), (b'07:00', b'07:00'), (b'08:00', b'08:00'), (b'09:00', b'09:00'), (b'10:00', b'10:00'), (b'11:00', b'11:00'), (b'12:00', b'12:00'), (b'13:00', b'13:00'), (b'14:00', b'14:00'), (b'15:00', b'15:00'), (b'16:00', b'16:00'), (b'17:00', b'17:00'), (b'18:00', b'18:00'), (b'19:00', b'19:00'), (b'20:00', b'20:00'), (b'21:00', b'21:00'), (b'22:00', b'22:00'), (b'23:00', b'23:00'), (b'24:00', b'24:00'), (b'01:00', b'01:00'), (b'02:00', b'02:00'), (b'03:00', b'03:00'), (b'04:00', b'04:00'), (b'05:00', b'05:00')])),
                ('closetime', models.CharField(default=b'22:00', max_length=10, verbose_name=b'Close Time', choices=[(b'06:00', b'06:00'), (b'07:00', b'07:00'), (b'08:00', b'08:00'), (b'09:00', b'09:00'), (b'10:00', b'10:00'), (b'11:00', b'11:00'), (b'12:00', b'12:00'), (b'13:00', b'13:00'), (b'14:00', b'14:00'), (b'15:00', b'15:00'), (b'16:00', b'16:00'), (b'17:00', b'17:00'), (b'18:00', b'18:00'), (b'19:00', b'19:00'), (b'20:00', b'20:00'), (b'21:00', b'21:00'), (b'22:00', b'22:00'), (b'23:00', b'23:00'), (b'24:00', b'24:00'), (b'01:00', b'01:00'), (b'02:00', b'02:00'), (b'03:00', b'03:00'), (b'04:00', b'04:00'), (b'05:00', b'05:00')])),
                ('baseUser', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RestaurantComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField()),
                ('restaurant', models.ForeignKey(to='business.Restaurant')),
            ],
        ),
        migrations.AddField(
            model_name='dish',
            name='restaurant',
            field=models.ForeignKey(to='business.Restaurant'),
        ),
        migrations.AddField(
            model_name='address',
            name='restaurant',
            field=models.ForeignKey(related_name='address', to='business.Restaurant'),
        ),
    ]
