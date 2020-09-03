import os
import pprint

from pymongo import MongoClient, IndexModel, ASCENDING, DESCENDING

from crawler import spotifycli
from crawler.collectors.top_songs import SpotifyTopSongs
from crawler.collectors.top_songs import UtamapTopSongs
from crawler.collectors.utamap import get_utamap_lyrics
from crawler.collectors.uta_net import get_uta_net_lyrics

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')


def main():
    c = MongoClient(host='localhost', port=27017)

    music_1_artist_1 = IndexModel([("music", ASCENDING), ("artist", ASCENDING)])
    music_1 = IndexModel([("music", ASCENDING)])
    artist_1 = IndexModel([("artist", ASCENDING)])

    c.music_kanji.music.create_indexes([music_1_artist_1,
                                        music_1,
                                        artist_1])

    c.spotify.music.create_indexes([music_1_artist_1,
                                    music_1,
                                    artist_1])

    spotify = spotifycli.SpotifyClient(CLIENT_ID, CLIENT_SECRET)
    spotify_auth = spotify.auth()
    pprint.pprint(spotify_auth.search('椎名林檎', market='JP'))

    spotify_top_songs = SpotifyTopSongs(country='jp', recurrence='weekly', date='2020-03-05')
    data = spotify_top_songs.get_data()

    for song in data:
        c.spotify.music.insert_one(song)

    utamap_top_songs = UtamapTopSongs(recurrence='daily', date='2020-08-27')
    data = utamap_top_songs.get_data()

    for song in data:
        c.music_kanji.music.insert_one(song)

    utamap_top_songs = UtamapTopSongs(recurrence='weekly', date='2020-08-26')
    data = utamap_top_songs.get_data()

    for song in data:
        c.music_kanji.music.insert_one(song)
        # print(get_utamap_lyrics(song['URL']))


if __name__ == '__main__':
    main()

# TODO MAKE CRAWLER ASYNC
