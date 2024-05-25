import requests
from config import API_KEY
import xml.etree.ElementTree as ET

BASE_URL = "http://apis.data.go.kr/6410000/busstationservice/getBusStationList"

def get_station_list(station_name):
    params = {
        'serviceKey': API_KEY,
        'keyword': station_name
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        response_content = response.content.decode('utf-8')
        print(response_content)  # 디버그를 위해 응답 내용 출력
        return response_content
    else:
        print(f"Error: {response.status_code}")  # 에러 코드 출력
        return None

def parse_station_list(xml_data):
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

        bus_station_list = msg_body.findall("busStationList")
        results = []
        for station in bus_station_list:
            result = {
                "stationId": station.find("stationId").text,
                "stationName": station.find("stationName").text,
                "mobileNo": station.find("mobileNo").text if station.find("mobileNo") is not None else "N/A",
                "regionName": station.find("regionName").text,
                "x": station.find("x").text,
                "y": station.find("y").text,
            }
            results.append(result)
        
        return results

    except ET.ParseError as e:
        print(f"XML Parse Error: {e}")
        return []
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return []

if __name__ == '__main__':
    station_name = input("Enter the station name: ")
    station_list = get_station_list(station_name)
    if station_list:
        parsed_list = parse_station_list(station_list)
        if parsed_list:
            for station in parsed_list:
                print(f"Station ID: {station['stationId']}, Name: {station['stationName']}, Mobile No: {station['mobileNo']}, Region: {station['regionName']}, Coordinates: ({station['x']}, {station['y']})")
        else:
            print("No stations found.")
    else:
        print("Failed to retrieve station information.")
