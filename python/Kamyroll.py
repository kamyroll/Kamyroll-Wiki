""""
Project: PythonClient
Script: Kamyroll.py
Author: hyugogirubato
Date: 2023.01.08
"""

import sys
import time
import requests

USER_AGENT = 'Kamyroll/4.1.0 Android/7.1.2 okhttp/4.9.2'
APP_TOKEN = 'HMbQeThWmZq4t7w'


# channel_id = ['adn', 'neko-sama', 'crunchyroll']


def eprint(value):
    print(f"ERROR: {value}")
    sys.exit(1)


class Client:

    def __init__(self, channel_id='crunchyroll', locale='en-US'):
        self.locale = locale
        self.api = 'https://api.kamyroll.tech'
        # self.api = 'http://localhost:3000'
        self.bearer_expire = 0
        self.bearer_token = None
        if channel_id in self.platforms()['items']:
            self.channel_id = channel_id
        else:
            eprint('The selected channel_id is unavailable or invalid.')

    def _makeRequest(self, url, method='GET', params=None, data=None, json=None, headers=None, authorization=None):
        method = 'GET ' if method is None else method.upper()
        if headers is None:
            headers = {'accept': '*/*', 'user-agent': USER_AGENT}

        if authorization == 'BEARER':
            if self.bearer_expire <= time.time():
                self.getToken()
            headers['authorization'] = f"Bearer {self.bearer_token}"

        if params is None:
            params = {}
        else:
            params['channel_id'] = self.channel_id
            params['locale'] = self.locale

        r = requests.request(method=method, url=url, params=params, data=data, json=json, headers=headers)
        if not r.ok:
            eprint(r.content.decode('utf-8'))
        return r

    def platforms(self):
        return self._makeRequest(f"{self.api}/auth/v1/platforms", method='GET').json()

    def getToken(self, device_id='whatvalueshouldbeforweb', device_type='com.service.data'):
        params = {'device_id': device_id, 'device_type': device_type, 'access_token': APP_TOKEN}
        j_response = self._makeRequest(f"{self.api}/auth/v1/token", params=params, method='GET').json()
        self.bearer_token = j_response['access_token']
        self.bearer_expire = j_response['expires_in']
        return j_response

    def search(self, query, limit=100):
        params = {'query': query, 'limit': limit}
        return self._makeRequest(f"{self.api}/content/v1/search", params=params, method='GET', authorization='BEARER').json()

    def seasons(self, series_id, filter=None):
        params = {'id': series_id}
        if not filter is None:
            params['filter'] = filter
        return self._makeRequest(f"{self.api}/content/v1/seasons", params=params, method='GET', authorization='BEARER').json()

    def media(self, media_id):
        params = {'id': media_id}
        return self._makeRequest(f"{self.api}/content/v1/media", params=params, method='GET', authorization='BEARER').json()

    def movies(self, movies_id):
        params = {'id': movies_id}
        return self._makeRequest(f"{self.api}/content/v1/movies", params=params, method='GET', authorization='BEARER').json()

    def streams(self, media_id, format='ass', type='adaptive_hls'):
        params = {'id': media_id, 'format': format, 'type': type}
        return self._makeRequest(f"{self.api}/videos/v1/streams", params=params, method='GET', authorization='BEARER').json()

    def updated(self, limit=20):
        params = {'limit': limit}
        return self._makeRequest(f"{self.api}/content/v1/updated", params=params, method='GET', authorization='BEARER').json()

    def info(self):
        return self._makeRequest(f"{self.api}/auth/v1/info", method='GET', authorization='BEARER').json()
