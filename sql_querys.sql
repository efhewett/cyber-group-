USE SpaceWeatherDB3;

-- View data from Geomagnetic Storms
SELECT * FROM GeomagneticStorms;

-- View data from Linked Events for Geomagnetic Storms
SELECT * FROM LinkedEvents_GST;

-- View data from Solar Flares
SELECT * FROM SolarFlares;

-- View data from Instruments linked to Solar Flares
SELECT * FROM Instruments;

-- View data from Linked Events for Solar Flares
SELECT * FROM LinkedEvents_FLR;

-- View data from Geomagnetic Storm Kp Index
SELECT * FROM GeomagneticStormKpIndex;

-- View data from API Requests
SELECT * FROM ApiRequests;
