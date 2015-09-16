from django.db import models
from django.core.validators import RegexValidator
from django.core.urlresolvers import reverse

from geopy.geocoders.googlev3 import GoogleV3
from geopy.exc import GeocoderQueryError
from urllib2 import URLError

from OrderingSystem import settings


class Restaurant(models.Model):
    baseUser = models.OneToOneField(settings.AUTH_USER_MODEL)
    name = models.CharField('Restaurant Name', max_length=50)
    # category = models.CharField('Food Type', max_length=50, blank=True)
    msg = models.TextField('Description', blank=True, null=True)
    image = models.FileField(upload_to='restaurant/%Y/%m/%d', null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^[+|\d][0-9() -]*\d$', message="Please enter a correct phone number.")
    phone = models.CharField('Business Phone', validators=[phone_regex], null=True, blank=True, max_length=20)
    Provide_Delivery = models.BooleanField(default=False)
    Children_Friendly = models.BooleanField(default=False)
    Wifi = models.BooleanField(default=False)
    Vegan = models.BooleanField(default=False)
    Gluten_Free = models.BooleanField(default=False)

    # time reference
    createdAt = models.DateTimeField(auto_now_add=1, auto_now=0)
    lastAccessAt = models.DateTimeField(auto_now=1, auto_now_add=0)
    food_choices = (
        ('ff', 'FastFood'),
        ('cns', 'Chinese'),
        ('jpf', 'Japanese'),
        ('wst', 'Western'),
    )
    category = models.CharField('Food Type', max_length=10, choices=food_choices, default='cns')

    time_choices = (
        ('06:00', '06:00'),
        ('07:00', '07:00'),
        ('08:00', '08:00'),
        ('09:00', '09:00'),
        ('10:00', '10:00'),
        ('11:00', '11:00'),
        ('12:00', '12:00'),
        ('13:00', '13:00'),
        ('14:00', '14:00'),
        ('15:00', '15:00'),
        ('16:00', '16:00'),
        ('17:00', '17:00'),
        ('18:00', '18:00'),
        ('19:00', '19:00'),
        ('20:00', '20:00'),
        ('21:00', '21:00'),
        ('22:00', '22:00'),
        ('23:00', '23:00'),
        ('24:00', '24:00'),
        ('01:00', '01:00'),
        ('02:00', '02:00'),
        ('03:00', '03:00'),
        ('04:00', '04:00'),
        ('05:00', '05:00'),
    )
    opentime = models.CharField('Open Time', max_length=10, choices=time_choices, default='08:00')
    closetime = models.CharField('Close Time', max_length=10, choices=time_choices, default='22:00')

    def get_absolute_url(self):
        return reverse('business:RestaurantPage')


class Address(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name="address")
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=20)
    zipcode = models.CharField(max_length=10)
    # gis = gis_models.GeoManager()

    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    # location = gis_models.PointField(u"longitude/latitude", geography=True, blank=True, null=True)

    def __unicode__(self):
        return str(self.latitude) + " " + str(self.longitude)

    def save(self, **kwargs):
        address = u'%s %s, %s %s' % (self.address, self.city, self.state, self.zipcode)
        address = address.encode('utf-8')
        try:
            response = GoogleV3().geocode(address)

        except (URLError, GeocoderQueryError, ValueError):
            pass
        else:
            if response:
                _, coordinates = response
                self.latitude = coordinates[0]
                self.longitude = coordinates[1]
            else:
                self.latitude = None
                self.longitude = None
                # point = "POINT(%s %s)" % (coordinates[1], coordinates[0])
                # self.location = geos.fromstr(point)

        super(Address, self).save()


class Dish(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    name = models.CharField(max_length=50)
    price = models.FloatField()
    image = models.FileField(upload_to='dishes/%Y/%m/%d', blank=True, null=True)
    liked = models.IntegerField(default=0)
    unliked = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)

    type_choices = (
        ('ent', 'Entries'),
        ('mai', 'Main'),
        ('des', 'Dessert'),
        ('drk', 'Drinks'),
    )
    dishcategory = models.CharField('Dish Type', max_length=10, choices=type_choices, default='ent')


class RestaurantComment(models.Model):
    comment = models.TextField()
    restaurant = models.ForeignKey(Restaurant)


class DishComment(models.Model):
    comment = models.TextField()
    dish = models.ForeignKey(Dish)
