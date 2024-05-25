import requests
from xml.etree import ElementTree as ET
from config import SERVICE_KEY  # API 키를 가져옵니다.

def get_bus_arrival_info(station_id):
    if not station_id:
        return None
    url = 'http://apis.data.go.kr/6410000/busarrivalservice/getBusArrivalList'
    params = {
        'serviceKey': SERVICE_KEY,
        'stationId': station_id
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        result_code = root.findtext('.//resultCode')
        if result_code == '0':
            arrival_items = root.findall('.//busArrivalList')
            results = []
            for item in arrival_items:
                results.append({
                    'stationId': item.findtext('stationId'),
                    'routeId': item.findtext('routeId'),
                    'locationNo1': item.findtext('locationNo1'),
                    'predictTime1': item.findtext('predictTime1'),
                    'remainSeatCnt1': item.findtext('remainSeatCnt1'),
                    'locationNo2': item.findtext('locationNo2'),
                    'predictTime2': item.findtext('predictTime2')
                })
            return results
        else:
            print(f"Error: {root.findtext('.//resultMessage')}")
            return None
    else:
        print(f"HTTP Error: {response.status_code}")
        return None

def get_route_info(route_id):
    url = 'http://apis.data.go.kr/6410000/busrouteservice/getBusRouteInfoItem'
    params = {
        'serviceKey': SERVICE_KEY,
        'routeId': route_id
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        result_code = root.findtext('.//resultCode')
        if result_code == '0':
            bus_route_info_item = root.find('.//busRouteInfoItem')
            return {
                'routeId': bus_route_info_item.findtext('routeId'),
                'routeName': bus_route_info_item.findtext('routeName'),
                'routeTypeName': bus_route_info_item.findtext('routeTypeName'),
                'startStationName': bus_route_info_item.findtext('startStationName'),
                'endStationName': bus_route_info_item.findtext('endStationName')
            }
        else:
            print(f"Error: {root.findtext('.//resultMessage')}")
            return None
    else:
        print(f"HTTP Error: {response.status_code}")
        return None

def pretty_print_xml(xml_str):
    import xml.dom.minidom
    dom = xml.dom.minidom.parseString(xml_str)
    pretty_xml_as_string = dom.toprettyxml()
    print(pretty_xml_as_string)

if __name__ == '__main__':
    station_info = get_bus_arrival_info('203000399')
    print(station_info)
