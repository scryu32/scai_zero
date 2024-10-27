#날씨 가져오는 코드임
#forecast()하면 사용됨
#지금은 현재 날씨밖에 못가져오는데 나중에 내일날씨나 시간같은거 넣을수 있을듯

import requests
from datetime import datetime
import xmltodict
import os

keys = os.environ.get('WEATHER_KEY')

def get_current_date():
    current_date = datetime.now().date()
    return current_date.strftime("%Y%m%d")

def get_current_hour():
    now = datetime.now()
    return datetime.now().strftime("%H%M")

int_to_weather = {
    "0": "맑음",
    "1": "비",
    "2": "비/눈",
    "3": "눈",
    "5": "빗방울",
    "6": "빗방울눈날림",
    "7": "눈날림"
}

def forecast():
    params ={'serviceKey' : keys, 
        'pageNo' : '1', 
        'numOfRows' : '10', 
        'dataType' : 'XML', 
        'base_date' : get_current_date(), 
        'base_time' : get_current_hour(),
        'nx' : '55', 
        'ny' : '127' }
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
    res = requests.get(url, params)

    xml_data = res.text
    dict_data = xmltodict.parse(xml_data)

    for item in dict_data['response']['body']['items']['item']:
        if item['category'] == 'T1H':
            temp = item['obsrValue']
        if item['category'] == 'PTY':
            sky = item['obsrValue']
            
    sky = int_to_weather[sky]
    
    return temp , sky

print(forecast())