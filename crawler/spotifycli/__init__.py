import requests
import base64


class SpotifyClient:
    def __init__(self, client_id, client_secret):
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__base64_credentials = base64.b64encode(f'{client_id}:{client_secret}'.encode())

    def auth(self):
        params = {'grant_type': 'client_credentials'}
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {self.__base64_credentials}'
        }
        response = requests.post('https://accounts.spotify.com/api/token', json=params, headers=headers).json()

        return SpotifyClientAuthenticated(self.__client_id, self.__client_secret, response)


class SpotifyClientAuthenticated(SpotifyClient):
    def __init__(self, client_id, client_secret, token_info):
        super().__init__(client_id, client_secret)
        self.__token = token_info['access_token']
        self.__type = token_info['token_type']
        self.__expiration = token_info['expires_in']
        self.__scope = token_info['scope']
