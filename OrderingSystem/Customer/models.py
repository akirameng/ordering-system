from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from OrderingSystem import settings


class Order(models.Model):
    restaurant = models.ForeignKey('business.Restaurant', related_name='restaurant')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='order')
    time = models.DateTimeField()
    location = models.CharField(max_length=200)
    delivery_type = models.IntegerField()
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    discount = models.FloatField()
    paid = models.BooleanField(default=False)

    status_choices = (
        ('can', 'Cancelled'),
        ('prog', 'In Progress'),
        ('fin', 'Complete'),
    )
    status = models.CharField(max_length=10, choices=status_choices, default='prog')

    def __unicode__(self):
        return self.restaurant.name + ": " + str(self.id)


class OrderItem(models.Model):
    Order = models.ForeignKey(Order, related_name='orderitem')
    Dish = models.ForeignKey('business.Dish')
    restaurant = models.ForeignKey('business.Restaurant')
    number = models.IntegerField(validators=[MinValueValidator(0)])


class Comment_R(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comment_r')
    restaurant = models.ForeignKey('business.Restaurant')
    text = models.TextField()
    time = models.DateTimeField()
    rating = models.FloatField(validators=[MinValueValidator(1.0), MaxValueValidator(5.0)])
