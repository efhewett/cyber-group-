-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS SpaceWeatherDB;
USE SpaceWeatherDB;

-- Create table for Geomagnetic Storms
CREATE TABLE IF NOT EXISTS GeomagneticStorms (
    gstID VARCHAR(255) PRIMARY KEY,
    startTime DATETIME NOT NULL,
    endTime DATETIME,
    dataSource VARCHAR(50),
    INDEX idx_gst_start_time (startTime)
);

-- Create table for Linked Events for Geomagnetic Storms
CREATE TABLE IF NOT EXISTS LinkedEvents_GST (
    linkID INT AUTO_INCREMENT PRIMARY KEY,
    gstID VARCHAR(255),
    activityID VARCHAR(255),
    FOREIGN KEY (gstID) REFERENCES GeomagneticStorms(gstID),
    INDEX idx_linkedEvents_gstID (gstID)
);

-- Create table for Solar Flares
CREATE TABLE IF NOT EXISTS SolarFlares (
    flrID VARCHAR(255) PRIMARY KEY,
    beginTime DATETIME NOT NULL,
    peakTime DATETIME,
    endTime DATETIME,
    classType VARCHAR(50),
    sourceLocation VARCHAR(50),
    activeRegionNum INT,
    dataSource VARCHAR(50),
    INDEX idx_flare_beginTime (beginTime)
);

-- Create table for Instruments linked to Solar Flares
CREATE TABLE IF NOT EXISTS Instruments (
    instrumentID INT AUTO_INCREMENT PRIMARY KEY,
    flrID VARCHAR(255),
    displayName VARCHAR(255),
    FOREIGN KEY (flrID) REFERENCES SolarFlares(flrID),
    INDEX idx_instruments_flrID (flrID)
);

-- Create table for Linked Events for Solar Flares
CREATE TABLE IF NOT EXISTS LinkedEvents_FLR (
    linkID INT AUTO_INCREMENT PRIMARY KEY,
    flrID VARCHAR(255),
    activityID VARCHAR(255),
    FOREIGN KEY (flrID) REFERENCES SolarFlares(flrID),
    INDEX idx_linkedEvents_flrID (flrID)
);

-- Create table for Geomagnetic Storm Kp Index
CREATE TABLE IF NOT EXISTS GeomagneticStormKpIndex (
    gst_kp_id INT AUTO_INCREMENT PRIMARY KEY,
    gstID VARCHAR(255),
    observedTime DATETIME NOT NULL,
    kpIndex INT NOT NULL CHECK (kpIndex >= 0),
    source VARCHAR(50),
    FOREIGN KEY (gstID) REFERENCES GeomagneticStorms(gstID),
    INDEX idx_gst_kpIndex_gstID (gstID),
    INDEX idx_gst_kpIndex_observedTime (observedTime)
);

-- Create table for API Requests
CREATE TABLE IF NOT EXISTS ApiRequests (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    endpoint VARCHAR(255) NOT NULL,
    request_time DATETIME NOT NULL,
    response_status VARCHAR(50),
    response_content TEXT,
    INDEX idx_api_request_time (request_time)
);

CREATE TABLE testtable (
    id INT AUTO_INCREMENT PRIMARY KEY,
    column1 VARCHAR(255),
    column2 VARCHAR(255)
);
