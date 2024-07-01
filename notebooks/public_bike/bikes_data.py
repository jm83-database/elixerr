def data_preprocessing():
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    plt.rc('font', family='Malgun Gothic') # 차트에 한글 글자 깨짐 방지
    # 데이터 부르기
    bikes = pd.DataFrame()
    for i in range(3):
        bikes_temp = pd.read_csv(f'../../data/public_bike/서울특별시 공공자전거 대여정보_201906_{i+1}.csv', encoding='cp949', parse_dates=['대여일시'])
        bikes=pd.concat([bikes, bikes_temp])
        
    # 누락값 검사
    bikes.isnull().sum()

    # 파생변수, '요일', '일자', '대여시간대', '주말구분'
    요일 = ['월','화','수','목','금','토','일']
    요일순서 = ['월','화','수','목','금','토','일']
    bikes['요일'] = bikes['대여일시'].dt.day_of_week.apply(lambda x : 요일[x])
    bikes['대여시간대'] = bikes['대여일시'].dt.hour
    bikes['일자'] = bikes['대여일시'].dt.day
    bikes['주말구분'] = bikes['대여일시'].dt.day_of_week.apply(lambda x: '평일' if x < 5 else '주말')

    # 위도, 경도 파일 Merge
    bike_shop = pd.read_csv('../../data/public_bike/공공자전거 대여소 정보(23.06월 기준).csv', encoding='euc-kr')
    bikes_gu = bike_shop[['자치구', '대여소 번호', '보관소(대여소)명', '위도', '경도']]
    bikes_gu = bikes_gu.rename(columns={'보관소(대여소)명':'대여소명', '대여소 번호' : '대여소번호'})
    bikes = pd.merge(bikes, bikes_gu, left_on='대여 대여소번호', right_on='대여소번호')
    bikes = bikes.rename(columns={'자치구':'대여구','위도' : '대여점위도','경도' : '대여점경도'})

    return bikes

if __name__ == '__main__':
    data_preprocessing()