# pandas 이용
import pandas as pd
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore') # 파일 오류 무시
plt.rc('font', family='Malgun Gothic') # 차트에 한글 글자 깨짐 방지


# 1~13페이지까지 추출
df = pd.DataFrame()
for page_num in range(1,14,1):
    url = f'https://land.naver.com/news/trendReport.naver?page={page_num}'
    temp_num = pd.read_html(url, encoding='utf-8')
    df = pd.concat([df,temp_num[0]])

# % 제거
df_cp = df.copy()
df_cp = df_cp['제목'].str.replace('%', "")

# 전국, 서울, 수도권 제거
regions = ['전국', '서울', '수도권']
for region in regions:
    df_cp = df_cp.str.replace(region, '')

# ]를 중심으로 컬럼 구분 후 필요한 컬럼 선택
df_cp = df_cp.str.split(']', expand=True)
df_cp = df_cp[1]

# ,를 기준으로 분리
df_cp = df_cp.str.split(',', expand=True)

# 선택된 정보 저장
df_selected = df_cp.copy()

# str → float 자료형 변환
df_selected = df_selected.astype('float')

# 컬럼명 바꾸기
df_selected = df_selected.rename(columns={0:'전국', 1:'서울', 2:'수도권'})

# 데이터 병합
df[regions] = df_selected

# 데이터 선택
df_rate = df[['등록일']+regions+['번호']]

# 데이터 정렬
df_rate = df_rate[::-1]

# 차트 그리기
df_rate.head(30).plot(x = '등록일', y = regions, figsize = (15,6), title = '2019.07~2020.01 추이 분석')
plt.show()

# datetime 변환
df_rate['등록일'] = pd.to_datetime(df_rate['등록일'])

# 월별 추이 분석(평균)
montly_analysis = df_rate.groupby(df_rate.등록일.dt.month)[['전국', '서울', '수도권']].mean()
montly_analysis.plot(figsize = (15,6), title = '월별 추이 분석')
plt.show()

# 년도별 추이 분석(평균)
yearly_analysis = df_rate.groupby(df_rate.등록일.dt.year)[['전국', '서울', '수도권']].mean()
yearly_analysis.plot(figsize = (15,6), title = '년도별 추이 분석')
plt.show()