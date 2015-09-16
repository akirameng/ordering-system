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

from django.conf.urls import patterns
from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required

import views

urlpatterns = patterns(
    '',
    url(r'^$', login_required(views.RestaurantView.as_view()), name='RestaurantPage'),
    url(r'^report$', login_required(views.ReportView.as_view()), name='ReportPage'),
    url(r'^edit$', login_required(views.EditRestaurantView.as_view()), name='EditRestaurantPage'),
    url(r'^dish/(?P<pk>[0-9]+)$', login_required(views.DishView.as_view()), name='DishPage'),
    url(r'^order/(?P<pk>[0-9]+)$', login_required(views.OrderView.as_view()), name='OrderPage'),
    url(r'^order$', login_required(views.OrderListView.as_view()), name='OrderListPage'),
    url(r'^order/inprogress/$', login_required(views.InprocessOrderView.as_view()), name='InprogressOrderPage'),
    url(r'^order/complete/$', login_required(views.CompleteOrderView.as_view()), name='CompleteOrderPage'),
    url(r'^order/cancel/$', login_required(views.CanceledOrderView.as_view()), name='CancelOrderPage'),
    url(r'^signup$', views.SignUpView.as_view(), name='SignUpPage'),
    url(r'^account/(?P<pk>[0-9]+)$', login_required(views.BuyerView.as_view()), name='BuyerPage'),
    )
