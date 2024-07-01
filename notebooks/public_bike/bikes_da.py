def bikes_da():
    import streamlit as st
    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sns
    import folium
    import streamlit.components.v1 as components
    plt.rc('font', family='Malgun Gothic') # 차트에 한글 글자 깨짐 방지

    @st.cache_data
    def data_preprocessing():
        # 데이터 부르기
        bikes = pd.DataFrame()
        for i in range(3):
            bikes_temp = pd.read_csv(f'../data/public_bike/서울특별시 공공자전거 대여정보_201906_{i+1}.csv', encoding='cp949', parse_dates=['대여일시'])
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
        bike_shop = pd.read_csv('../data/public_bike/공공자전거 대여소 정보(23.06월 기준).csv', encoding='euc-kr')
        bikes_gu = bike_shop[['자치구', '대여소 번호', '보관소(대여소)명', '위도', '경도']]
        bikes_gu = bikes_gu.rename(columns={'보관소(대여소)명':'대여소명', '대여소 번호' : '대여소번호'})
        bikes = pd.merge(bikes, bikes_gu, left_on='대여 대여소번호', right_on='대여소번호')
        bikes = bikes.rename(columns={'자치구':'대여구','위도' : '대여점위도','경도' : '대여점경도'})

        return bikes


    bikes=data_preprocessing()

    tab1, tab2, tab3, tab4 =  st.tabs(['데이터 보기', '시간적 분석', '공간적 분석', '인기대여소'])

    with tab1:
        st.dataframe(bikes.head(20))
        
    with tab2:
        chart_name = ['요일','일자','대여시간대']
        for i in chart_name:
            fig, ax = plt.subplots(figsize=(15,4))
            ax = sns.countplot(data=bikes, x=i)
            ax.set_title(f'{i}별 이용건수')
            st.pyplot(fig)

        st.markdown('''
                    1. 요일별 분석
                    * 평일보다 주말에 따릉이 이용건수가 많고 주말 중에서는 토요일에 가장 이용건수가 많다
                    * 주말에 인기 있는 대여소 근처에 대여소를 추가로 설치하거나 따릉이를 추가 배치할 필요가 있다.
                    
                    2. 일자별 분석
                    * 6일이 현충일이이지만 비가 와서 이용건수가 적다. 강수량에 영향을 많이 받는다.
                    * 일회용 우비 등을 비치해서 비 오는 날도 따릉이 이용에 불편이 없도록 한다.
                    
                    3. 시간대별 분석
                    * 출퇴근 시간대를 중심으로 이용건수가 많고 오전<오후<저녁 순으로 이용건수가 증가한다.
                    * 출퇴근 시간대에 많이 이용되는 대여소에 따릉이를 추가 배치가 필요하다.
                    ''')
        hourly_dayofweek_ride = bikes.pivot_table(index='대여시간대',columns='요일',values='자전거번호',aggfunc='count')
        daily_gu_use = bikes.pivot_table(index='일자', columns='대여구', values='자전거번호', aggfunc='count')
        fig, ax = plt.subplots(figsize=(15,8))
        ax = sns.heatmap(hourly_dayofweek_ride, annot=True, fmt='d')
        ax.set_title('대여시간대 & 요일별 이용건수')
        st.pyplot(fig)
        
        
    with tab3:
        hourly_gu_use = bikes.pivot_table(index='대여시간대', columns='대여구', values='자전거번호', aggfunc='count')
        daily_gu_use = bikes.pivot_table(index='일자', columns='대여구', values='자전거번호', aggfunc='count')
        chart_name = [hourly_gu_use,daily_gu_use]
        for  i in chart_name:
            fig, ax = plt.subplots(figsize=(10,8))
            ax = sns.heatmap(i.T)
            ax.set_title(f'{i.index.name} & 구별 이용건수')
            st.pyplot(fig)

        st.markdown('''
                    1. 대여시간별 분석
                    * 영등포구, 송파구, 마포구, 강남구, 강서구 5개 자치구가 따릉이 이용건수가 많다.
                    * 해당 자치구들 중 어떤 대여소가 인기 있는지 확인이 필요하다.
                    
                    2. 일자별 분석
                    * 8일, 22일이 주말인데 모든 자치구가 전체적으로 이용 건수가 많다.
                    * 평일과 주말을 구분하여 이용건수가 높은 자치구들에 따릉이 배치를 조정해야할 필요가 있다.
                    ''')
        
    with tab4:
        st.write('tab4')
        rent_bike = bikes.pivot_table(index=['대여 대여소명','대여점위도','대여점경도'],columns=['주말구분'],values='자전거번호',aggfunc='count')
        weekend_favorites50 = rent_bike.nlargest(50,'주말')[['주말','평일']].reset_index()
        days_favorites50 = rent_bike.nlargest(50,'평일')[['주말','평일']].reset_index()
        map = folium.Map( location=[bikes['대여점위도'].mean(), bikes['대여점경도'].mean()], zoom_start=11)
        for i in weekend_favorites50.index:
            sub_lat = weekend_favorites50.loc[i,'대여점위도']
            sub_lon = weekend_favorites50.loc[i,'대여점경도']
            name = weekend_favorites50.loc[i,'대여 대여소명']
            iframe = "<pre><b>대여소 이름:</b><br>"+str(name)+"</pre>" # 팝업창 텍스트
            popup = folium.Popup(iframe, min_width=100, max_width=500) # 팝업창 크기 조절
            folium.Marker(
                location=[sub_lat, sub_lon],
                popup=popup,
                tooltip=name
            ).add_to(map)

        for i, row in days_favorites50.iterrows():
            sub_lat = row['대여점위도']
            sub_lon = row['대여점경도']
            name = row['대여 대여소명']
            iframe = "<pre><b>대여소 이름:</b><br>"+str(name)+"</pre>" # 팝업창 텍스트
            popup = folium.Popup(iframe, min_width=100, max_width=500) # 팝업창 크기 조절
            folium.Marker(
                location=[sub_lat, sub_lon],
                popup=popup,
                tooltip=name, 
                icon=folium.Icon(color = 'red', icon = 'star')
            ).add_to(map)
        
        st.subheader('주말과 평일 인기 대여소 Top50')
        st.caption('''주말과 평일에 인기 있는 대여소 Top50을 표시한 것으로 주로 한강변, 호수나 공원 근처이다. 파랑색 마커는 주말, 빨강색 마커는 평일이다.''')
        # 지도 시각화, streamlit
        components.html(map._repr_html_(), height=400)
