__author__ = 'JC'
from django.core.files.base import ContentFile
from requests import request, ConnectionError


def save_profile_picture(backend, user, response, details, is_new=False, *args, **kwargs):
    if not user.image:
        if backend.name == 'google-oauth2':
            if response.get('image') and response['image'].get('url'):
                url = response['image'].get('url')
                try:
                    response = request('GET', url)
                    response.raise_for_status()
                except ConnectionError:
                    pass

        elif backend.name == 'facebook':   # and is_new:
            url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
            try:
                response = request('GET', url, params={'type': 'large'})
                response.raise_for_status()
            except ConnectionError:
                pass
        user.image.save(user.username + '_avatar.jpg', ContentFile(response.content), save=False)
        user.save()
