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

from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from views import modal_login

import views

urlpatterns = patterns(
    '',
    url(r'^$', login_required(views.ProfileView.as_view()), name='profilePage'),
    url(r'^activities/$', login_required(views.ActivityView.as_view()), name='activityPage'),
    url(r'^modal-login/$', modal_login, {'template_name': 'registration/modal-login.html'}, name='modal_login'),
    url(r'^success', login_required(views.LoginSuccessView.as_view()), name='loginSuccessPage'),
    url(r'^orders/$', login_required(views.CustomerOrderView.as_view()), name='orderPage'),
    url(r'^orders/(?P<pk>[0-9]+)$', login_required(views.Detail.as_view()), name='orderdetail'),
    )
