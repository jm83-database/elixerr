import datetime
import pandas as pd

# 원하는 식당명을 받습니다.
restaurant_id = input("원하는 식당명을 입력해주세요 : ")

# 기준일을 지정합니다.
startday = datetime.datetime.strptime("2024-07-21", '%Y-%m-%d')
# 오늘 날짜를 가져옵니다.
today = datetime.datetime.today()

# 오늘 날짜와 기준일의 차이를 계산합니다.
deltatime = today - startday
deltatime_to_int = deltatime.days # range에 넣기 위해 int로 변환

sundays = []
# 오늘부터 2주 단위로 일요일을 표시합니다.
for i in range(0, deltatime_to_int+7, 14):
    sunday = startday + datetime.timedelta(days=i)
    sundays.append(sunday)

result = sundays[-1]
print(f'{restaurant_id}이/가 쉬는 가까운 일요일은 {result.year}-{result.month}-{result.day}입니다.')