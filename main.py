import xml.etree.ElementTree as ET
from io import BytesIO

import pandas as pd
import requests
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime
from db_utils import insert_data
from graph import get_gms_data, get_sf_data

matplotlib.use('Agg')

class NasaApiFetcher:
    def __init__(self, api_key):
        self.api_key = api_key

    def log_api_request(self, endpoint, status_code, response_content):
        data = {
            'endpoint': endpoint,
            'request_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'response_status': f'{status_code}',
            'response_content': str(response_content)
        }
        insert_data('ApiRequests', data)

    def fetch_data(self, url, params=None):
        response = requests.get(url, params=params, timeout=15)
        if response.status_code == 200:
            self.log_api_request(url, response.status_code, response.json())
            return response.json()
        else:
            self.log_api_request(url, response.status_code, response.text)
            return None

class SolarFlareFetcher(NasaApiFetcher):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.endpoint = 'https://api.nasa.gov/DONKI/FLR'

    def format_datetime(self, dt_str):
        try:
            return datetime.strptime(dt_str, '%Y-%m-%dT%H:%MZ').strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            return None

    def get_flare_data(self, start_date, end_date):
        payload = {
            'startDate': start_date,
            'endDate': end_date,
            'api_key': self.api_key
        }
        return self.fetch_data(self.endpoint, params=payload)

    def insert_flares(self, start_date, end_date):
        flares = self.get_flare_data(start_date, end_date)
        if flares:
            for flare in flares:
                begin_time = self.format_datetime(flare.get('beginTime'))
                peak_time = self.format_datetime(flare.get('peakTime'))
                end_time = self.format_datetime(flare.get('endTime'))
                flare_data = {
                    'flrID': flare.get('flrID'),
                    'beginTime': begin_time,
                    'peakTime': peak_time,
                    'endTime': end_time,
                    'classType': flare.get('classType'),
                    'sourceLocation': flare.get('sourceLocation', ''),
                    'activeRegionNum': flare.get('activeRegionNum', None),
                    'dataSource': 'NASA'
                }
                insert_data('SolarFlares', flare_data)

                for instrument in flare.get('instruments', []):
                    instrument_data = {
                        'flrID': flare.get('flrID'),
                        'displayName': instrument.get('displayName')
                    }
                    insert_data('Instruments', instrument_data)

                linked_events = flare.get('linkedEvents')
                if linked_events:
                    for event in linked_events:
                        linked_event_data = {
                            'flrID': flare.get('flrID'),
                            'activityID': event.get('activityID')
                        }
                        insert_data('LinkedEvents_FLR', linked_event_data)

class AuroraBorealisWatch:
    def __init__(self, url):
        self.url = url

    def fetch_data(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            return None

    def parse_data(self, xml_data):
        try:
            root = ET.fromstring(xml_data)
            status = root.findtext('status')
            message = root.findtext('message')
            data = {
                'status': status,
                'message': message,
            }
            return data
        except ET.ParseError:
            return None

class GeoStormFetcher(NasaApiFetcher):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.endpoint = 'https://api.nasa.gov/DONKI/GST'

    def format_datetime(self, dt_str):
        try:
            return datetime.strptime(dt_str, '%Y-%m-%dT%H:%MZ').strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            return None

    def get_geostorm_data(self, start_date, end_date):
        payload = {
            'startDate': start_date,
            'endDate': end_date,
            'api_key': self.api_key
        }
        return self.fetch_data(self.endpoint, params=payload)

    def insert_geostorms(self, start_date, end_date):
        storms = self.get_geostorm_data(start_date, end_date)
        if storms:
            for storm in storms:
                start_time = self.format_datetime(storm.get('startTime'))
                storm_data = {
                    'gstID': storm.get('gstID'),
                    'startTime': start_time,
                    'dataSource': storm.get('source')
                }
                insert_data('GeomagneticStorms', storm_data)

                for kp_index in storm['allKpIndex']:
                    kp_index_data = {
                        'gstID': storm.get('gstID'),
                        'observedTime': self.format_datetime(kp_index.get("observedTime")),
                        'kpIndex': kp_index.get("kpIndex"),
                        'source': kp_index.get("source")
                    }
                    insert_data('GeomagneticStormKpIndex', kp_index_data)

                linked_events = storm.get('linkedEvents')
                if linked_events:
                    for event in linked_events:
                        linked_event_data = {
                            'gstID': storm.get('gstID'),
                            'activityID': event.get('activityID')
                        }
                        insert_data('LinkedEvents_GST', linked_event_data)

class GraphGenerator:
    @staticmethod
    def generate_graph():
        plt.style.use('Solarize_Light2')

        solar_flares = get_sf_data()
        geo_storms = get_gms_data()

        solar_flare_dates = [solar_flare.peak_time for solar_flare in solar_flares]
        geo_dates = [geo_storm.obs_time for geo_storm in geo_storms]

        x1_sf_dates = pd.DataFrame({'Date': solar_flare_dates})
        x2_gms_dates = pd.DataFrame({'Date': geo_dates})

        y1_sf_activity = [solar_flare.get_activity_level() for solar_flare in solar_flares]
        y2_gms_activity = [geo_storm.get_activity_level() for geo_storm in geo_storms]

        plt.scatter(x1_sf_dates, y1_sf_activity, color="blue", label="Solar Flares")
        plt.scatter(x2_gms_dates, y2_gms_activity, color="red", label="Geomagnetic Storms")

        plt.plot(x1_sf_dates, y1_sf_activity, color="blue", label="Solar Flares")
        plt.plot(x2_gms_dates, y2_gms_activity, color="red", label="Geomagnetic Storms")

        plt.title("Solar Flare and Geomagnetic Storm Activity")
        plt.xlabel("Dates")
        plt.ylabel("Activity Level")

        plt.legend()

        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        return buf

if __name__ == "__main__":
    api_key = "7QynoyZpCrwiFnXJA7koYDcjll4Xszom1Ez8iCnF"
    solar_flare_fetcher = SolarFlareFetcher(api_key)
    solar_flare_fetcher.insert_flares("2024-02-22", "2024-08-22")

    geo_storm_fetcher = GeoStormFetcher(api_key)
    geo_storm_fetcher.insert_geostorms("2024-02-22", "2024-08-22")
