import requests
from datetime import datetime
from datetime import timedelta

from crawler.utils import csv_to_json
# from crawler.exceptions import params TODO: CREATE EXPLICIT EXCEPTION


AVAILABLE_COUNTRIES = ['global', 'br', 'jp']  # TODO: ADD ALL AVAILABLE COUNTRIES


class SpotifyTopArtists:
    def __init__(self, country='global', recurrence='daily', date='latest'):
        if country not in AVAILABLE_COUNTRIES:
            raise Exception  # TODO: CREATE EXPLICIT EXCEPTION

        if recurrence not in ['daily', 'weekly']:
            raise Exception  # TODO: CREATE EXPLICIT EXCEPTION

        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            if date == 'latest':
                pass
            else:
                raise Exception  # TODO: CREATE EXPLICIT EXCEPTION

        if recurrence == 'weekly' and date != 'latest':
            final_date = datetime.strptime(date, '%Y-%m-%d')
            start_date = final_date - timedelta(days=7)
            date = f'{start_date.strftime("%Y-%m-%d")}-{final_date.strftime("%Y-%m-%d")}'

        self.__url = f'https://spotifycharts.com/regional/{country}/{recurrence}/{date}'

    def get_data(self):
        data_url = f'{self.__url}/download'
        data = requests.get(data_url).text
        data = csv_to_json(data)

        return data
