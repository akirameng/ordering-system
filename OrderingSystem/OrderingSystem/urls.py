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
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from accounts.forms import RegistrationForm
from registration.backends.default.views import RegistrationView

urlpatterns = patterns(
    '',
    url(r'^accounts/register/$', RegistrationView.as_view(form_class=RegistrationForm), name='registration_register'),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^business/', include('business.urls', namespace='business')),
    url(r'^', include('Customer.urls', namespace='Customer')),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
