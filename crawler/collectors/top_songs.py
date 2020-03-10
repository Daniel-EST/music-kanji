import requests
import re
from datetime import datetime
from datetime import timedelta

from crawler.utils import parse_csv
from crawler.exceptions import InvalidCountry
from crawler.exceptions import InvalidRecurrence
from crawler.exceptions import InvalidDate


AVAILABLE_COUNTRIES = ['global', 'br', 'jp']  # TODO: ADD ALL AVAILABLE COUNTRIES


class SpotifyTopSongs:
    def __init__(self, country='global', recurrence='daily', date='latest'):
        if country not in AVAILABLE_COUNTRIES:
            raise InvalidCountry

        elif recurrence not in ['daily', 'weekly']:
            raise InvalidRecurrence

        elif recurrence == 'daily':
            if date != 'latest':
                try:
                    datetime.strptime(date, '%Y-%m-%d')
                except ValueError:
                    raise InvalidDate

        elif recurrence == 'weekly':
            final_date = datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)
            start_date = final_date - timedelta(days=7)
            date = f'{start_date.strftime("%Y-%m-%d")}--{final_date.strftime("%Y-%m-%d")}'

        self.__url = f'https://spotifycharts.com/regional/{country}/{recurrence}/{date}'

    def get_data(self):
        headers = {
            'User-Agent': """Mozilla/5.0 (Windows NT 10.0; Win64; x64)""",
            'Cache - Control': 'no-cache'
        }
        data_url = f'{self.__url}/download'
        csv_string = requests.get(data_url, headers).text
        csv_string = re.sub(",,,.*\n", '', csv_string)
        data = parse_csv(csv_string)

        return data
