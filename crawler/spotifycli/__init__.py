import requests
import base64

from crawler.exceptions import InvalidCredentials


class SpotifyClient:
    def __init__(self, client_id, client_secret):
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__base64_credentials = base64.b64encode(f'{client_id}:{client_secret}'.encode())\
            .decode("utf-8")

    def auth(self):
        params = {'grant_type': 'client_credentials'}
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {self.__base64_credentials}'
        }
        response = requests.post('https://accounts.spotify.com/api/token', data=params, headers=headers)
        if response.status_code != 200:
            raise InvalidCredentials
        else:
            response_body = response.json()

        return SpotifyClientAuthenticated(self.__client_id, self.__client_secret, response_body)


class SpotifyClientAuthenticated(SpotifyClient):
    def __init__(self, client_id, client_secret, token_info):
        super().__init__(client_id, client_secret)
        self.__token = token_info['access_token']
        self.__type = token_info['token_type']
        self.__expiration = token_info['expires_in']
        self.__scope = token_info['scope']

    def search(self, query, tp='artist', market='US', limit=10, offset=5):
        params = {
            'q': query,
            'type': tp,
            'market': market,
            'limit': limit,
            'offset': offset
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.__token}',
        }

        response = requests.get('https://api.spotify.com/v1/search', params=params, headers=headers)

        return response.json()
