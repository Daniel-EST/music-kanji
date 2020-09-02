import os
import pprint

from crawler import spotifycli
from crawler.collectors.top_songs import SpotifyTopSongs
from crawler.collectors.top_songs import UtamapTopSongs

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')


def main():
    spotify_top_songs = SpotifyTopSongs(country='jp', recurrence='weekly', date='2020-03-05')
    data = spotify_top_songs.get_data()
    for song in data:
        print(song)

    utamap_top_songs = UtamapTopSongs(recurrence='daily', date='2020-08-27')
    data = utamap_top_songs.get_data()
    for song in data:
        print(song)

    utamap_top_songs = UtamapTopSongs(recurrence='weekly', date='2020-08-26')
    data = utamap_top_songs.get_data()
    for song in data:
        print(song)

    spotify = spotifycli.SpotifyClient(CLIENT_ID, CLIENT_SECRET)
    spotify_auth = spotify.auth()
    pprint.pprint(spotify_auth.search('Muse', tp='artist'))


if __name__ == '__main__':
    main()
