#날씨 가져오는 코드임
#forecast()하면 사용됨

import requests
from datetime import datetime, timedelta
import xmltodict
import os

keys = os.environ.get('WEATHER_KEY')

#기본값 0, 0 1일전이면 -1, 2시간전이면 -2 알잘딱해서 넣자 리턴값은 튜플임
def get_datetime(days=0, hours=0, minutes=0):
    adjusted_datetime = datetime.now() + timedelta(days=days, hours=hours, minutes=minutes)
    formatted_date = adjusted_datetime.strftime("%Y%m%d")
    formatted_hour = adjusted_datetime.strftime("%H%M")
    return formatted_date, formatted_hour

int_to_weather = {
    "0": "맑음",
    "1": "비",
    "2": "비/눈",
    "3": "눈",
    "5": "빗방울",
    "6": "빗방울눈날림",
    "7": "눈날림"
}

def forecast(days=0, hours=0, minutes=0):
    params ={'serviceKey' : keys, 
        'pageNo' : '1', 
        'numOfRows' : '10', 
        'dataType' : 'XML', 
        'base_date' : get_datetime(days, hours, minutes)[0], 
        'base_time' : get_datetime(days, hours, minutes)[1],
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
