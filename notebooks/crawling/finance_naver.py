# pandas 이용
import pandas as pd
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore') # 파일 오류 무시
plt.rc('font', family='Malgun Gothic') # 차트에 한글 글자 깨짐 방지



# 여러 국가의 환율을 1~10페이지까지 추출
currency_code = int(input('통화유형을 선택해주세요(0:USD, 1:EUR, 2:JPY): '))
currency_type = ['USD', 'EUR', 'JPY']
currency_name = ['미국 달러', '유럽연합 유로', '일본 엔(100)']
currency_symbols = ['$','€', '¥']
selected = currency_type[currency_code]
df_selected = pd.DataFrame()
for page_num in range(1,11,1):
    url = f'https://finance.naver.com/marketindex/exchangeDailyQuote.naver?marketindexCd=FX_{selected}KRW&page={page_num}'
    temp_num = pd.read_html(url, encoding='cp949', header = 1)
    df_selected = pd.concat([df_selected,temp_num[0]])


    
# 원하는 열만 선택
df_selected = df_selected.drop(['전일대비'],axis=1)
#데이터 재정렬
df_selected = df_selected[::-1].reset_index(drop=True)
#데이터 표시
print(f'''==={currency_name[currency_code]} - {selected}({currency_symbols[currency_code]})===
{df_selected.head(10)}
''')



# 전체 차트 작성
df_total_chart = df_selected.copy()
df_total_chart = df_total_chart.set_index('날짜')
# df_total_chart = df_total_chart[::-1]
df_total_chart ['매매기준율'].plot(figsize=(15,6), title = 'exchange rate') # figsize 단위는 inch
plt.show()


# 월별 차트 작성
# 날짜 데이터 str → datetime 변환
df_selected['날짜'] = df_selected['날짜'].str.replace(".",'').astype('datetime64[ms]')

# 월 파생변수 생성
df_selected['월'] = df_selected['날짜'].dt.month
month_in = int(input('검색할 월입력(예:9): '))
month_df = df_selected.loc[df_selected['월'] == month_in].drop('월', axis=1)

# 월별 데이터 표시
print(f'''==={currency_name[currency_code]} - {selected}({currency_symbols[currency_code]})===
{month_df.head(10)}
''')

# 차트를 그릴 데이터셋 복제
month_df_chart = month_df.copy()
month_df_chart = month_df_chart.set_index('날짜')

# 선택한 달의 매매기준율 차트 그리기
month_df_chart['매매기준율'].plot()
plt.show()