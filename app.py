from flask import Flask, jsonify, render_template, request, send_file
from datetime import date, timedelta
from main import NasaApiFetcher, SolarFlareFetcher, AuroraBorealisWatch, GeoStormFetcher, GraphGenerator

# NASA API key
# To get your NASA API key sign up here: https://api.nasa.gov/
NASA_API_KEY = ''

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/nasa-photo', methods=['GET'])
def nasa_photo():
    ASPOD_API_URL = f'https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}'
    fetcher = NasaApiFetcher(NASA_API_KEY)
    data = fetcher.fetch_data(ASPOD_API_URL)
    if data:
        return jsonify({
            'url': data['url'],
            'title': data['title'],
            'explanation': data['explanation']
        })
    else:
        return jsonify({'error': 'Failed to retrieve photo of the day'}), 404

@app.route('/aurora-watch', methods=['GET'])
def get_aurora_borealis_data():
    AURORA_URL = 'http://aurorawatch.lancs.ac.uk/api/0.1/status.xml'
    fetcher = AuroraBorealisWatch(AURORA_URL)
    xml_data = fetcher.fetch_data()

    if xml_data:
        aurora_data = fetcher.parse_data(xml_data)
        return jsonify(aurora_data)
    else:
        return jsonify({'error': 'Unable to fetch Aurora Borealis data.'}), 500

@app.route('/nasa-geostorm', methods=['GET', 'POST'])
def get_geostorm_data():
    start_date = request.args.get('start_date', (date.today() - timedelta(days=30)).strftime('%Y-%m-%d'))
    end_date = request.args.get('end_date', date.today().strftime('%Y-%m-%d'))

    fetcher = GeoStormFetcher(NASA_API_KEY)
    if request.method == 'POST':
        fetcher.insert_geostorms(start_date, end_date)
        return jsonify({"message": "Geomagnetic storms data updated successfully"})

    data = fetcher.get_geostorm_data(start_date, end_date)
    if data:
        kp_indexes = []
        for event in data:
            kp_values = [kp['kpIndex'] for kp in event.get('allKpIndex', [])]
            kp_indexes.append({
                'gstID': event.get('gstID'),
                'kpIndexes': kp_values
            })
        return jsonify(kp_indexes)
    else:
        return jsonify({'error': 'Failed to retrieve geostorm data'}), 404

@app.route('/nasa-solarflare', methods=['GET', 'POST'])
def get_solar_flare_data():
    start_date = request.args.get('start_date', (date.today() - timedelta(days=30)).strftime('%Y-%m-%d'))
    end_date = request.args.get('end_date', date.today().strftime('%Y-%m-%d'))

    fetcher = SolarFlareFetcher(NASA_API_KEY)
    if request.method == 'POST':
        fetcher.insert_flares(start_date, end_date)
        return jsonify({"message": "Solar flares data updated successfully"})

    solar_flare_data = fetcher.get_flare_data(start_date, end_date)
    if solar_flare_data:
        flares = [{
            'flrID': flare.get('flrID'),
            'beginTime': flare.get('beginTime'),
            'peakTime': flare.get('peakTime'),
            'endTime': flare.get('endTime'),
            'classType': flare.get('classType'),
            'sourceLocation': flare.get('sourceLocation'),
            'activeRegionNum': flare.get('activeRegionNum')
        } for flare in solar_flare_data]
        return jsonify(flares)
    else:
        return jsonify({'error': 'Failed to retrieve solar flare data'}), 404

@app.route('/plot.png')
def plot_png():
    img = GraphGenerator.generate_graph()
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
