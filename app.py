from flask import Flask, render_template, request
import requests
import xml.etree.ElementTree as ET
from config import API_KEY

app = Flask(__name__)

BASE_URL = "http://apis.data.go.kr/6410000/busarrivalservice/getBusArrivalList"

def get_bus_arrival_list(station_id):
    params = {
        'serviceKey': API_KEY,
        'stationId': station_id
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        response_content = response.content.decode('utf-8')
        print(response_content)  # 디버그를 위해 응답 내용 출력
        return response_content
    else:
        print(f"Error: {response.status_code}")  # 에러 코드 출력
        return None

def parse_bus_arrival_list(xml_data):
    try:
        root = ET.fromstring(xml_data)
        result_code = root.find("./msgHeader/resultCode").text
        if result_code != '0':
            result_message = root.find("./msgHeader/resultMessage").text
            print(f"API Error: {result_code}, {result_message}")
            return []

        msg_body = root.find("msgBody")
        if msg_body is None:
            print("No msgBody found in the response.")
            return []

        bus_arrival_list = msg_body.findall("busArrivalList")
        results = []
        for bus in bus_arrival_list:
            result = {
                "stationId": bus.find("stationId").text,
                "routeId": bus.find("routeId").text,
                "locationNo1": bus.find("locationNo1").text,
                "predictTime1": bus.find("predictTime1").text,
                "lowPlate1": bus.find("lowPlate1").text,
                "plateNo1": bus.find("plateNo1").text,
                "remainSeatCnt1": bus.find("remainSeatCnt1").text,
                "locationNo2": bus.find("locationNo2").text if bus.find("locationNo2") is not None else "N/A",
                "predictTime2": bus.find("predictTime2").text if bus.find("predictTime2") is not None else "N/A",
                "lowPlate2": bus.find("lowPlate2").text if bus.find("lowPlate2") is not None else "N/A",
                "plateNo2": bus.find("plateNo2").text if bus.find("plateNo2") is not None else "N/A",
                "remainSeatCnt2": bus.find("remainSeatCnt2").text if bus.find("remainSeatCnt2") is not None else "N/A",
                "staOrder": bus.find("staOrder").text,
                "flag": bus.find("flag").text,
            }
            results.append(result)
        
        return results

    except ET.ParseError as e:
        print(f"XML Parse Error: {e}")
        return []
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return []

@app.route('/', methods=['GET', 'POST'])
def index():
    station_id = request.form.get('station_id', '203000400')
    bus_arrival_list_xml = get_bus_arrival_list(station_id)
    bus_arrival_list = parse_bus_arrival_list(bus_arrival_list_xml) if bus_arrival_list_xml else []
    if bus_arrival_list:
        for bus in bus_arrival_list:
            print(f"Route ID: {bus['routeId']}, 1st Bus Location: {bus['locationNo1']}, 1st Bus Arrival: {bus['predictTime1']} min, "
                  f"1st Bus Low Plate: {bus['lowPlate1']}, 1st Bus Plate No: {bus['plateNo1']}, 1st Bus Seats: {bus['remainSeatCnt1']}, "
                  f"2nd Bus Location: {bus['locationNo2']}, 2nd Bus Arrival: {bus['predictTime2']} min, 2nd Bus Low Plate: {bus['lowPlate2']}, "
                  f"2nd Bus Plate No: {bus['plateNo2']}, 2nd Bus Seats: {bus['remainSeatCnt2']}, Station Order: {bus['staOrder']}, Flag: {bus['flag']}")
    return render_template('index.html', bus_arrival_list=bus_arrival_list, station_id=station_id)

if __name__ == '__main__':
    app.run(debug=True)
