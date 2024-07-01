import streamlit as st

def get_exchange_rate_data(selected, currency_name):

    import pandas as pd
    import warnings
    import matplotlib.pyplot as plt
    warnings.filterwarnings('ignore') # 파일 오류 무시
    plt.rc('font', family='Malgun Gothic') # 차트에 한글 글자 깨짐 방지
    df_selected = pd.DataFrame()
    for page_num in range(1,6,1):
        url = f'https://finance.naver.com/marketindex/exchangeDailyQuote.naver?marketindexCd=FX_{selected}KRW&page={page_num}'
        temp_num = pd.read_html(url, encoding='cp949', header = 1)
        df_selected = pd.concat([df_selected,temp_num[0]])
    total_rate_data_view(df_selected, selected, currency_name)


def total_rate_data_view(df_selected, selected, currency_name):
    # 원하는 열만 선택
    df_selected = df_selected.drop(['전일대비'],axis=1)
    #데이터 재정렬
    df_selected = df_selected[::-1].reset_index(drop=True)
    
    st.subheader(f'{currency_name} : {selected}')
    st.dataframe(df_selected.head(20))
    
    #데이터 표시1
    # print(f'''==={currency_name[currency_code-1]} - {selected}({currency_symbols[currency_code-1]})===
    # {df_selected.head(10)}
    # ''')

    # 전체 차트 작성
    df_total_chart = df_selected.copy()
    df_total_chart = df_total_chart.set_index('날짜')
    # df_total_chart = df_total_chart[::-1]
    ax = df_total_chart ['매매기준율'].plot(figsize=(15,6), title = 'Total Exchange Rate') # figsize 단위는 inch
    fig = ax.get_figure()
    st.pyplot(fig)
    # plt.show()
    # month_rate_data_view(df_selected)


# def month_rate_data_view(df_selected):
#     # 월별 차트 작성
# # 날짜 데이터 str → datetime 변환
#     df_selected['날짜'] = df_selected['날짜'].str.replace(".",'').astype('datetime64[ms]')

#     # 월 파생변수 생성
#     df_selected['월'] = df_selected['날짜'].dt.month
#     month_in = int(input('검색할 월입력(예:9): '))
#     month_df = df_selected.loc[df_selected['월'] == month_in].drop('월', axis=1)

#     # 월별 데이터 표시
#     print(f'''==={currency_name[currency_code-1]} - {selected}({currency_symbols[currency_code-1]})===
#     {month_df.head(10)}
#     ''')

#     # 차트를 그릴 데이터셋 복제
#     month_df_chart = month_df.copy()
#     month_df_chart = month_df_chart.set_index('날짜')

#     # 선택한 달의 매매기준율 차트 그리기
#     month_df_chart['매매기준율'].plot()
#     plt.show()
    


def exchange_main():
    # 여러 국가의 환율을 1~10페이지까지 추출
    currency_symbols_name = {'미국 달러 ($)': 'USD', '유럽연합 유로 (€)': 'EUR','일본 엔(100) (¥)': 'JPY'}
    
    currency_name = st.selectbox('통화 선택', currency_symbols_name.keys())
    selected = currency_symbols_name[currency_name]
    clicked = st.button('환율 데이터 가져오기')        
    if clicked:
        get_exchange_rate_data(selected, currency_name) # 클릭 시 환율 데이터 불러오기 실행
    
    
if __name__ == '__main__':
    exchange_main()