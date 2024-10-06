from io import BytesIO
import pandas as pd
from matplotlib import pyplot as plt
import mysql.connector
from config import USER, PASSWORD, HOST

class SolarFlare:
    def __init__(self, class_type, peak_time):
        self.class_type = class_type
        self.peak_time = peak_time

    def get_activity_level(self):
        sf_level = {"A": 3, "B": 4, "C": 5, "M1": 6, "M2": 7, "M3": 8,  "X": 9}
        activity_level = self.class_type[0]
        if activity_level == "M":
            number = float(self.class_type[1:2])
            if number < 3:
                activity_level = "M1"
            elif number < 6:
                activity_level = "M2"
            else:
                activity_level = "M3"
        return sf_level[activity_level]

class GeoStorm:
    def __init__(self, obs_time, kp_index):
        self.obs_time = obs_time
        self.kp_index = kp_index

    def get_activity_level(self):
        return self.kp_index

class DbConnectionError(Exception):
    pass

def connect_to_db(db_name):
    cnx = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=db_name)
    return cnx

def get_sf_data():
    try:
        db_name = "SpaceWeatherDB"
        db_connection = connect_to_db(db_name)
    except Exception:
        raise DbConnectionError('Failed to connect to the database')
    try:
        cur = db_connection.cursor()

        query = "SELECT ClassType, PeakTime FROM SolarFlares WHERE PeakTime >= now()-interval 3 month"
        cur.execute(query)

        results = cur.fetchall()
        all_solar_flares = []
        for result in results:
            solar_flare = SolarFlare(result[0], result[1])
            all_solar_flares.append(solar_flare)

        cur.close()

    except Exception:
        raise DbConnectionError("Failed to read data from the database.")

    finally:
        if db_connection:
            db_connection.close()

    return all_solar_flares

def get_gms_data():
    try:
        db_name = "SpaceWeatherDB"
        db_connection = connect_to_db(db_name)
    except Exception:
        raise DbConnectionError('Failed to connect to the database')
    try:
        cur = db_connection.cursor()

        query = "SELECT observedTime, kpIndex FROM GeomagneticStormKpIndex WHERE observedTime >= now()-interval 3 month"
        cur.execute(query)

        results = cur.fetchall()
        all_geo_storms = []
        for result in results:
            geo_storm = GeoStorm(result[0], result[1])
            all_geo_storms.append(geo_storm)

        cur.close()

    except Exception:
        raise DbConnectionError("Failed to read data from the database.")

    finally:
        if db_connection:
            db_connection.close()

    return all_geo_storms
