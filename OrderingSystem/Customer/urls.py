"""OrderingSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from Customer import views
from django.contrib.auth.decorators import login_required

urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='homepage'),
    #url(r'^restaurant$', views.RestaurantView.as_view(), name='restaurantPage'),
    url(r'^(?P<pk>[0-9]+)/order$', login_required(views.OrderView.as_view()), name='orderPage'),
    url(r'^(?P<pk>[0-9]+)/complete$', login_required(views.CompleteOrderView.as_view()), name='completeOrder'),
    url(r'^restaurant/(?P<pk>[0-9]+)/$', views.RestaurantAPIView.as_view(), name='resaurant_detail_api'),
    url(r'^(?P<pk>[0-9]+)/$', views.RestaurantDetailView.as_view(), name='resaurant_detail'),
    url(r'^(?P<pk>[0-9]+)/dishlist$', views.DishListView.as_view(), name='resaurant_dishlist'),
    url(r'^dishlist/(?P<dish_id>[0-9]+)/$', views.DetailDish.as_view(), name='resaurant_detaildish'),
    url(r'^dishlist/(?P<dish_id>[0-9]+)/like$', views.DetailDishLike.as_view(), name='resaurant_detaildish_like'),
    url(r'^dishlist/(?P<dish_id>[0-9]+)/unliked$', views.DetailDishUnlike.as_view(), name='resaurant_detaildish_unlike'),
    url(r'^filter$', views.FilterView.as_view(), name='resaurant_filter'),
    url(r'^cookie/$',views.CookieView.as_view(),name="order_cookie"),
    url(r'^searchresult/$',views.search.as_view(),name="searchpage"),
    )

#urlpatterns = format_suffix_patterns(urlpatterns)
