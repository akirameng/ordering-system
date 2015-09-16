from django.contrib import admin

# Register your models here.
from models import *

admin.site.register(Restaurant)
admin.site.register(RestaurantComment)
admin.site.register(Address)
admin.site.register(Dish)
admin.site.register(DishComment)
