from flask import Flask, request, render_template
import xml.etree.ElementTree as ET
from config import SERVICE_KEY  # API 키를 가져옵니다.
from getData import get_route_info, get_bus_arrival_info

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    bus_info = None
    if request.method == 'POST':
        station_id = request.form.get('stationId')
        if station_id:
            bus_info_raw = get_bus_arrival_info(station_id)
            if bus_info_raw:
                bus_info = parse_bus_info(bus_info_raw)
    return render_template('index.html', bus_info=bus_info)

def parse_bus_info(bus_info_raw):
    buses = []
    for bus in bus_info_raw:
        route_id = bus['routeId']
        route_info = get_route_info(route_id)
        if route_info:
            buses.append({
                'route_number': route_info['routeName'],
                'location_no1': bus['locationNo1'],
                'predict_time1': bus['predictTime1'],
                'location_no2': bus.get('locationNo2'),
                'predict_time2': bus.get('predictTime2')
            })
    return buses

if __name__ == '__main__':
    app.run(debug=True)
