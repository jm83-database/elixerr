import datetime
import pandas as pd

print("환영합니다.\n2주 단위로 쉬는 일요일을 알려주는 프로그램입니다.")
# 원하는 식당명을 받습니다.
restaurant_id = input("입력하고 싶은 식당명을 입력해주세요 : ")

# 기준일을 입력합니다.
startday_input = input("기준일을 입력해주세요(예)20240721) : ")
startday_fomatting = startday_input[0:4] + '-' + startday_input[4:6] + '-' + startday_input[6:]
startday = datetime.datetime.strptime(startday_fomatting, '%Y-%m-%d')
# 오늘 날짜를 가져옵니다.
today = datetime.datetime.today()

# 오늘 날짜와 기준일의 차이를 계산합니다.
deltatime = today - startday
deltatime_to_int = deltatime.days # range에 넣기 위해 int로 변환

sundays = []
# 오늘을 기준으로 최근 쉬었던 일요일을 찾아줍니다.
for i in range(0, deltatime_to_int, 14):
    sunday = startday + datetime.timedelta(days=i)
    sundays.append(sunday)

past_sunday_off = sundays[-1]
next_sunday_off = past_sunday_off + datetime.timedelta(days=14)

text = f'''{restaurant_id}이/가 쉬었던 가까운 일요일은 {past_sunday_off.year}-{past_sunday_off.month}-{past_sunday_off.day}입니다.
다가오는 쉬는 날은 {next_sunday_off.year}-{next_sunday_off.month}-{next_sunday_off.day}입니다.
'''
print(text)