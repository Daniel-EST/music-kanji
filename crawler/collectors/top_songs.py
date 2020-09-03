import requests
import re
from datetime import datetime
from datetime import timedelta

from bs4 import BeautifulSoup

from crawler import Crawler
from crawler.utils import parse_spotify_csv
from crawler.exceptions import InvalidCountry
from crawler.exceptions import InvalidRecurrence
from crawler.exceptions import InvalidDate

AVAILABLE_COUNTRIES = ['global', 'us', 'gb', 'ar', 'at', 'au', 'be', 'bg', 'bo', 'br', 'ca', 'ch', 'cl', 'co', 'cr',
                       'cy', 'cz', 'de', 'dk', 'do', 'ec', 'ee', 'es', 'fi', 'fr', 'gr', 'gt', 'hk', 'hn', 'hu', 'id',
                       'ie', 'il', 'in', 'is', 'it', 'jp', 'lt', 'lu', 'lv', 'mx', 'my', 'ni', 'nl', 'no', 'nz', 'pa',
                       'pe', 'ph', 'pl', 'pt', 'py', 'ro', 'ru', 'se', 'sg', 'sk', 'sv', 'th', 'tr', 'tw', 'ua', 'uy',
                       'vn', 'za']


class SpotifyTopSongs(Crawler):
    def __init__(self, country='global', recurrence='daily', date='latest'):
        # TODO REFACTOR
        # TODO HANDLE DATE = LATEST WHEN RECURRENCE IS WEEKLY
        super().__init__()
        if country not in AVAILABLE_COUNTRIES:
            raise InvalidCountry

        elif recurrence not in ['daily', 'weekly']:
            raise InvalidRecurrence

        elif recurrence == 'daily':
            if date != 'latest':
                try:
                    self.__date = datetime.strptime(date, '%Y-%m-%d')
                    if self.__date > datetime.today():
                        raise InvalidDate(date)

                except ValueError:
                    raise InvalidDate(date)
            else:
                self.__date = datetime.now()

        elif recurrence == 'weekly':
            self.__date = datetime.strptime(date, '%Y-%m-%d')
            final_date = self.__date + timedelta(days=1)
            start_date = final_date - timedelta(days=7)
            date = f'{start_date.strftime("%Y-%m-%d")}--{final_date.strftime("%Y-%m-%d")}'

        self.__recurrence = recurrence
        self.__url = f'https://spotifycharts.com/regional/{country}/{recurrence}/{date}'

    def get_data(self):
        # TODO ERROR PROTECTION

        headers = {
            'User-Agent': """Mozilla/5.0 (Windows NT 10.0; Win64; x64)""",
            'Cache - Control': 'no-cache'
        }

        data_url = f'{self.__url}/download'
        csv_string = requests.get(data_url, headers).text
        csv_string = re.sub(r',,,.*\n', str(), csv_string)
        parsed_data = parse_spotify_csv(csv_string)

        for music_info in parsed_data:
            music_info['Recurrence'] = self.__recurrence
            music_info['date'] = self.__date
            music_info['date_collected'] = datetime.now()
            music_info['source'] = 'spotify'

            yield music_info


class UtamapTopSongs(Crawler):
    def __init__(self, recurrence='daily', date='latest'):
        # TODO REFACTOR
        super().__init__()
        if recurrence in ['daily', 'weekly', 'top500']:
            self.__recurrence = recurrence

            if date == 'latest':
                self.__date = datetime.today()

            else:
                try:
                    self.__date = datetime.strptime(date, '%Y-%m-%d')

                except ValueError:
                    raise InvalidDate(date)

                if self.__date > datetime.today():
                    raise InvalidDate(date)

                elif self.__date < datetime(2018, 9, 9):
                    raise InvalidDate(date)
        else:
            raise InvalidRecurrence

        self.__url = self.__get_url()

    def __get_url(self):
        if self.__recurrence == 'daily':
            url_date = self.__date.strftime("%Y%m%d")
            return f'http://access.utamap.com/ranking/index.php?d={url_date}'

        elif self.__recurrence == 'weekly':
            url_date = self.__date.strftime("%y%m%d")
            return f'http://ranking.utamap.com/accessranking/{url_date}accessranking.html'

        elif self.__recurrence == 'top500':
            url_date = self.__date.strftime("%Y")
            return f'http://ranking.utamap.com/{url_date}f/'

    def __get_data_daily(self):
        # TODO ERROR PROTECTION

        data = requests.get(self.__url).text
        soup = BeautifulSoup(data, 'html.parser')

        top_musics_table_selection = soup.find_all('tbody')[6]
        musics_info = top_musics_table_selection.find_all('tr')[1:]

        for position, music_info in enumerate(musics_info):
            music_info = music_info.find_all('td')
            music_artist = music_info[2].text.strip()
            music_name = music_info[1].text.strip()
            music_position = position + 1
            music_url = music_info[1].find('a').get('href').strip()

            music_info = {
                'Position': music_position,
                'Recurrence': self.__recurrence,
                'Track Name': music_name,
                'Artist': music_artist,
                'URL': music_url,
                'date': self.__date,
                'date_collected': datetime.now(),
                'source': 'utamap'
            }

            yield music_info

    def __get_data_weekly(self):
        # TODO ERROR PROTECTION

        r = requests.get(self.__url)
        r.encoding = 'shift-jis'
        data = r.text

        soup = BeautifulSoup(data, 'html.parser')

        top_musics_table_selection = soup.find_all('table')[2]
        musics_info = top_musics_table_selection.find_all('tr')[3:]

        for position, music_info in enumerate(musics_info):
            music_info = music_info.find_all('td')
            music_artist = music_info[2].text.strip()
            music_name = music_info[1].text.strip()
            music_position = position + 1
            music_url = music_info[1].find('a').get('href').strip()

            music_info = {
                'Position': music_position,
                'Recurrence': self.__recurrence,
                'Track Name': music_name,
                'Artist': music_artist,
                'URL': music_url,
                'date': self.__date,
                'date_collected': datetime.now(),
                'source': 'utamap'
            }

            yield music_info

    def __get_data_top500(self):
        # TODO TOP 500 RANKING DATA CRAWLER
        pass

    def get_data(self):
        if self.__recurrence == 'daily':
            return self.__get_data_daily()

        if self.__recurrence == 'weekly':
            return self.__get_data_weekly()

        if self.__recurrence == 'top500':
            return self.__get_data_top500()
