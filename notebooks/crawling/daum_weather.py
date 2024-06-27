from bs4 import BeautifulSoup
import requests


def get_weather_daum(location):
    base_url = 'https://search.daum.net/search?nil_suggest=btn&w=tot&DA=SBC&q=' # 기본 주소
    search_query = location + '+날씨'

    url = base_url + search_query

    html_weather = requests.get(url)
    soup_weather = BeautifulSoup(html_weather.text, 'lxml')

    txt_temp = soup_weather.select_one('strong.txt_temp').text
    txt_weather = soup_weather.select_one('span.txt_weather').text
    dl_weather = soup_weather.select('dl.dl_weather>dd')
    [wind_speed, humidity, pm10] = [x.text for x in dl_weather]
    return txt_temp, txt_weather, wind_speed, humidity, pm10


location = input('검색하고 싶은 지역의 동명을 적어주세요:')# 검색하고 싶은 지역

txt_temp, txt_weather, wind_speed, humidity, pm10 = get_weather_daum(location)

print(f'''--------[오늘의 날씨 정보]----------
설정지역: {location}
현재 기온: {txt_temp} 
기상상태: {txt_weather}
현재 풍속: {wind_speed}
현재 습도 : {humidity}
미세먼지 : {pm10}
''')