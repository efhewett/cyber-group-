# 🛰️✨CFGDegree Group 2 Project✨🛰️

## Overview

So far, this web application, built with Flask, provides three key functionalities:
1. Displays the NASA Photo of the Day.
2. Shows the current status of Aurora Borealis in the UK.
3. Shows the correlation between solar flares and geomagnetic storms.

## Features

- **NASA Photo of the Day**: Fetches and displays the daily photo from NASA's Astronomy Picture of the Day (APOD) API.
- **Aurora Borealis Status**: Retrieves and displays the current aurora activity status from a UK-based API.
- **Solar Flares**: Retrieves a list of solar flare activity within the last 30 days.
- **Geomagnetic Storms**: Retrieves a list of geomagnetic storm activity within the last 30 days. 

## Prerequisites

- Python 3.x
- Flask
- Requests
- xml.etree.ElementTree as ET
- BytesIO
- Matplotlib
- Matplotlib.pyplot as plt
- Datetime
- Pandas
- Mysql.connector
- NASA API Key: https://api.nasa.gov/

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/cbone95/CFG_Group_2_Project.git
    cd code
    ```

2. **Install the required Python packages using 'pip'**:

    ```bash
    pip install flask requests
    pip install mysql-connector-python
    pip install matplotlib
    pip install pandas

    ```
3. **Set up your environment**:
- Make sure that you have set up the configuration for your database in 'config.py', and that the database is running and accessible. 

4. **Run the application**:

    ```bash
    python app.py
    ```

   The application will start and be available at `http://127.0.0.1:5000/`.

## Running the Data Insertion Script

To send data to the database, run the `main.py` script:

    ```bash
    python main.py
    ```


## Application Structure

- `app.py`: The app.py sets up the core Flask application.
- `main.py`: The main.py is the starting point where the main functions are run.
- `config.py`: The config.py file contains database credentials.
- `db_utils.py`: The db_utils file provides utility functions for managing database connections, executing queries, and handling transactions.
- `index.html`: The HTML template for rendering the homepage.
- `style_test.css`: The style sheet specifies the homepage's presentation and styling.
- `graph.py`: Generates and displays visualisations of space weather data, such as solar flares and geomagnetic storms.

### `app.py`

- **`/`**: Renders the `index.html` template.
- **`/nasa-photo`**: Returns JSON data for NASA's Photo of the Day, including the photo URL, title, and explanation.
- **`/aurora-watch`**: Returns JSON data for the current aurora activity status, including station, current activity, previous activity, and last updated time.
- **`/nasa-geostorm`**: Returns JSON data for geomagnetic storm data for a specific date range using DONKI. 
- **`/nasa-solarflare`**: Returns JSON data for solar flare data for a specific date range, providing detailed information about each flare using DONKI

### `main.py`

- **`NasaApiFetcher` Class**: Handles API requests to NASA, logs request details, and retrieves data, with error handling and response logging.
- **`SolarFlareFetcher` Class**: Extends 'NasaApiFetcher' to fetch, format, and insert solar flare data into a database, including related instruments and events.
- **`AuroraBorealisWatch` Class**: Fetches and arses Aurora Borealis data from an XML API, returning the status and message.
- **`GeoStormFetcher` Class**: Extends 'NasaApiFetcher' to fetch and insert geomagnetic storm data into a database, including formatting of timestamps and KP indexes.
- **`GraphGenerator` Class**: Generates and returns a sample graph as a PNG image, saved to an in-memory buffer.

### `config.py`

- **`Host`**: Specifies the hostname of the database server.
- **`USER`**: Defines the username used to connect to the database.
- **`PASSWORD`**: Sets the password for the database user.
- **`DATABASE`**: Indicates the name of the database to connect to. 

### `db_utils.py`

- **`create_connection()`**: Establishes a connection to the MySQL database using settings from 'config.py'.
- **`close_connection(connection)`**: Closes the provided database connection if it is open.
- **`execute_query(query, params=None)`**: Executes a SQL query with optional parameters and returns the result or a success/failure status.
- **`fetch_data(query, params=None)`**: Executes a SELECT query and returns the fetched data as a list of rows.
- **`insert_data(table, data)`**: Inserts a dictionary of data into the specified database table.

### `index.html`

- **`<!DOCTYPE HTML>` to `<head>`**: Sets up the document type and includes metadata such as character encoding, viewpoint settings, and a link to an external stylesheet.
- **`<body>` Content**: Contains sections for displaying the NASA photo of the day, Aurora Borealis status, and a chart comparing geomagnetic storm and solar flare data.
- **`<script>` Section**: Defines JavaScript functions to fetch and display NASA photo and Aurora Borealis data asynchronously when the page loads. 

### `style_test.css`

- **`body` Styles**: Sets the overall font, background colour, text colour, and layout for the pay, centring content and removing default margins and padding.
- **`h1` Styles**: Adds top margin and sets the colour for the main heading.
- **`#photo-container` Styles**: Styles the container for the NASA photo with background colour, border radius, box shadow, padding, and centers the content.
- **`#nasa-photo` Styles**: Adjusts the appearance of the NASA photo with max-width, height auto, border radius, and margin.
- **`#photo-title` Styles**: Sets the font size, weight, and margins for the photo title.
- **`#photo-description` Styles**: Defines the font size and line height for the photo description.
- **`@media` Query**: Adjusts padding and font sizes for smaller screens (max-width: 600px) to ensure responsiveness.
- **`#aurora-container` and `.chart-container` Styles**: Apply similar styling as the '#photo-container' to the Aurora Borealis status and chart sections, including background colour, border radius, box shadow, padding, and centre.

### `graph.py`

- **`SolarFlare`**: Represents a solar flare event with attributes for its classification (class_type) and peak time (peak_time). Includes a method to determine the flare's activity level.
- **`GeoStorm`**: Represents a geomagnetic storm event with attributes for the observation time (obs_time) and the Kp index (kp_index). Includes a method to retrieve the storm's activity level.
- **`DbConnectionError`**: A custom exception class used to handle errors related to database connections.
- **`connect_to_db(db_name)`**: Establishes a connection to the specified MySQL database using credentials from the config module.
- **`get_sf_data()`**: Queries the SpaceWeatherDB database for solar flare data from the last three months and returns a list of SolarFlare objects.
- **`get_gms_data()`**: Queries the SpaceWeatherDB database for geomagnetic storm data from the last three months and returns a list of GeoStorm objects.

## Usage

- **Access the main page**: Go to `http://127.0.0.1:5000/` in your web browser.
- **The NASA Photo**: Will be displayed along with its title and description.
- **Aurora Borealis status**: Will show current activity and station location.
- **Solar Flare and Geomagnetic Storm Graph**: Will show the correlation between solar flares and geomagnetic storms.

## Example Output

- **NASA Photo of the Day**: An image with its title and description.
- **Aurora Borealis Status**: The current activity state and the station name.
- **Solar Flares**: A list of X and M solar flares
- **Geomagnetic Storm**: A list of geomagnetic storms.

## Running Tests

To ensure the system is functioning correctly, you can run each test file individually. Use the following commands to execute the tests:

    ```bash
   python test/test_app.py
   python test/test_db_utils.py
   python test/test_graph.py
   python test/test_main.py
    ```
## View data insertion in SQL tables 

Enter this Query on SQL after running main.py to see the data inserted into tables - please wait 30 seconds to fetch data

```USE SpaceWeatherDB3;

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
```



## Roadmap

- **Impact Descriptions**: A general overview of the impact of space weather on Earth systems and satellites will be provided. This will convey essential information, which will lead to the creation of visual/interactive simulations.
- **Predictive Capabilities and Alerts**: The next phase of the project will involve developing prediction models for solar flares and geomagnetic storms, allowing users to receive alerts about potential space weather events and their possible effects on Earth’s technology and infrastructure.
- **Educational Collaborations**: We plan to collaborate with educational institutions such as schools and universities to integrate this platform into their curriculum. This collaboration will enhance the educational value of the project, providing students and researchers with a practical tool for studying space weather and its implications.

## Help

**For any help with installations or for any queries relating to this, please contact the collaborators of this project**
- **Catriona Bone**: catriona.bone.1995@gmail.com
- **Vivien Croggon**: vivcrogs@gmail.com
- **Amy Crossan**: amycrossan1@gmail.com
- **Sophia Harley**: sophia.r.harley@gmail.com
- **Chelsea Hartley**: chelsea_hartley@hotmail.com
- **Ellen Hewett**: ellen.hewett@gmail.com

