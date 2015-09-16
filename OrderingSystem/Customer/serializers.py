from business.models import Dish, DishComment, Restaurant

from rest_framework import serializers


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ('restaurant', 'name', 'price', 'image', 'liked', 'unliked','description','dishcategory')


class DishCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DishComment
        fields = ('dish','comment')


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('name', 'msg', 'image', 'phone', 'Provide_Delivery', 'Children_Friendly', 'Wifi', 'Vegan', 'category', 'opentime', 'closetime')



