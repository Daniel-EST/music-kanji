import unittest
from unittest.mock import patch

from crawler.exceptions import InvalidCredentials
from crawler.spotifycli import SpotifyClient


class SpotifyClientTests(unittest.TestCase):
    @patch("requests.post")
    def test_auth_wrong_credentials(self, mock_post):
        mock_post.return_value.status_code = 400
        spotify_client = SpotifyClient("id", "secret")

        with self.assertRaises(InvalidCredentials):
            spotify_client.auth()
''

if __name__ == '__main__':
    unittest.main()

# TODO CREATE MORE INTEGRATION TESTS
